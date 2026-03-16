import json
import re

from agent.llm_client import get_llm_client
from agent.tools_config import tools_list
from tools.open_meteo import get_daily_forecast
from agent.validator import validate_forecast
from config import MODEL_NAME, logger


forecast_state = {
    "offset": 0,
    "chunk_size": 3,
    "last_coords": (None, None)
}


def extract_coordinates(text):

    if not isinstance(text, str):
        return None

    normalized = text.replace(",", ".")

    numbers = re.findall(r"-?\d+(?:\.\d+)?", normalized)

    if len(numbers) < 2:
        return None

    try:

        lat = float(numbers[0])
        lon = float(numbers[1])

        if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
            return None

        if lat < 0 and lon > 0:
            logger.warning(
                f"Coordenadas suspeitas: lat {lat} (sul) com lon {lon} (leste). Para Brasil, lon deveria ser negativa."
            )

        return lat, lon

    except Exception:
        return None


def extract_coordinates_from_history(history):

    if not history:
        return None

    for item in reversed(history):

        content = ""

        if isinstance(item, dict) and item.get("role") == "user":
            content = item.get("content", "")

        elif isinstance(item, (list, tuple)):
            content = item[0]

        if isinstance(content, list):
            content = content[0].get("text", "")

        coords = extract_coordinates(content)

        if coords:
            return coords

    return None


def format_weather_response(lat, lon, forecast_data):

    linhas = [f"Previsão do tempo para latitude {lat} e longitude {lon}:\n"]

    for dia in forecast_data:

        data = dia.get("data", "N/A")
        temp_max = dia.get("temp_max_celsius", "N/A")
        temp_min = dia.get("temp_min_celsius", "N/A")
        precipitacao = dia.get("precipitacao_mm", "N/A")

        linhas.append(
            f"{data} | Temperatura máxima: {temp_max}°C | Temperatura mínima: {temp_min}°C | Precipitação: {precipitacao} mm"
        )

    return "\n".join(linhas)


def run_agent(user_message, history=None):

    global forecast_state

    if not isinstance(user_message, str):
        user_message = str(user_message)

    logger.info(f"Iniciando processamento: {user_message}")

    detected_lat, detected_lon = (None, None)

    # Extração determinística da entrada do usuário
    user_coords = extract_coordinates(user_message)

    # --- ETAPA 1: TENTATIVA COM LLM ---

    try:

        client = get_llm_client()

        response = client.chat.completions.create(

            model=MODEL_NAME,

            messages=[
                {
                    "role": "system",
                    "content": """
Você é um assistente estrito de previsão do tempo.

REGRAS:
- Use a ferramenta APENAS se o usuário fornecer latitude e longitude numéricas.
- Nunca invente coordenadas.
- Se não houver números, não use a ferramenta.
"""
                },
                {"role": "user", "content": user_message}
            ],

            tools=tools_list,
            tool_choice="auto"
        )

        message = response.choices[0].message

        if message.tool_calls:

            logger.info("LLM identificou a necessidade da TOOL com sucesso.")

            tool_call = message.tool_calls[0]

            args = json.loads(tool_call.function.arguments)

            try:

                if args.get("lat") is not None:
                    detected_lat = float(args.get("lat"))

                if args.get("lon") is not None:
                    detected_lon = float(args.get("lon"))

                # --- NOVA PROTEÇÃO CONTRA ALTERAÇÃO DE COORDENADAS ---

                if user_coords:

                    user_lat, user_lon = user_coords

                    if (
                        abs(user_lat - detected_lat) > 0.01
                        or abs(user_lon - detected_lon) > 0.01
                    ):

                        logger.warning(
                            f"LLM alterou coordenadas do usuário: input=({user_lat},{user_lon}) tool=({detected_lat},{detected_lon})"
                        )

                        detected_lat, detected_lon = None, None

            except (ValueError, TypeError):

                logger.warning(
                    "LLM retornou coordenadas inválidas. Usando fallback."
                )

                detected_lat, detected_lon = None, None

        else:

            logger.info(
                "LLM não acionou tool_calls. Iniciando fallback determinístico."
            )

    except Exception as e:

        logger.warning(
            f"Erro na chamada do LLM: {e}. Prosseguindo para fallback."
        )

    # --- ETAPA 2: FALLBACK (REGEX + HISTÓRICO) ---

    if detected_lat is None or detected_lon is None:

        if user_coords:

            detected_lat, detected_lon = user_coords

            logger.info(
                f"Coordenadas extraídas via REGEX: lat={detected_lat}, lon={detected_lon}"
            )

        elif history:

            coords_hist = extract_coordinates_from_history(history)

            if coords_hist:

                detected_lat, detected_lon = coords_hist

                logger.info(
                    f"Coordenadas recuperadas do HISTÓRICO: lat={detected_lat}, lon={detected_lon}"
                )

    if detected_lat is None or detected_lon is None:

        return {
            "status": "erro",
            "mensagem": "Por favor, informe a latitude e longitude válidas (ex: -23.55 -46.63)."
        }

    # --- ETAPA 3: EXECUÇÃO ---

    current_coords = (detected_lat, detected_lon)

    if current_coords != forecast_state["last_coords"]:

        forecast_state["offset"] = 0
        forecast_state["last_coords"] = current_coords

    try:

        tool_result = get_daily_forecast(detected_lat, detected_lon, 10)

        if tool_result.get("status") != "sucesso":

            return {
                "status": "erro",
                "mensagem": "Erro ao consultar serviço meteorológico."
            }

        todas_previsoes = tool_result.get("previsao", [])

        start = forecast_state["offset"]

        if start >= len(todas_previsoes):

            return {
                "status": "erro",
                "mensagem": "Não há mais previsões disponíveis no momento."
            }

        end = start + forecast_state["chunk_size"]

        previsoes_chunk = todas_previsoes[start:end]

        forecast_state["offset"] += len(previsoes_chunk)

        resposta_formatada = format_weather_response(
            detected_lat,
            detected_lon,
            previsoes_chunk
        )

        if not validate_forecast(resposta_formatada, previsoes_chunk):

            logger.error("Validação falhou: divergência de dados.")

            return {
                "status": "erro",
                "mensagem": "Erro de integridade nos dados da previsão."
            }

        return {
            "status": "sucesso",
            "resposta": resposta_formatada
        }

    except Exception as e:

        logger.error(f"Erro no processamento final: {e}")

        return {
            "status": "erro",
            "mensagem": "Erro interno no agente."
        }


if __name__ == "__main__":

    msg1 = "Qual a previsão para -23.55 -46.63?"
    res1 = run_agent(msg1)

    print(f"TESTE 1: {res1.get('resposta') or res1.get('mensagem')}")

    historico_simulado = [
        {"role": "user", "content": "previsão para -23.55 -46.63"},
        {"role": "assistant", "content": res1.get('resposta', '')}
    ]

    msg2 = "e para os próximos dias?"
    res2 = run_agent(msg2, history=historico_simulado)

    print(f"\nTESTE 2: {res2.get('resposta') or res2.get('mensagem')}")