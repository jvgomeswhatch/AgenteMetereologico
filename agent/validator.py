import logging
import re

logger = logging.getLogger(__name__)

def validate_forecast(response_text: str, forecast_list: list, expected_lat: float = None, expected_lon: float = None) -> bool:
    """
    Verifica se os valores exibidos na resposta final correspondem
    aos valores da lista de previsões e se as coordenadas estão corretas.

    Args:
        response_text (str): texto final enviado ao usuário
        forecast_list (list): lista de dicionários com os dados da previsão
        expected_lat (float): latitude que o sistema DEVERIA ter usado
        expected_lon (float): longitude que o sistema DEVERIA ter usado
    """

    if not forecast_list:
        logger.warning("Validador recebeu uma lista de previsão vazia.")
        return False

    try:
        logger.info("Iniciando validação da integridade dos dados na resposta.")

        # --- NOVA TRAVA: VALIDAÇÃO DE COORDENADAS ---
        if expected_lat is not None and expected_lon is not None:
            # Busca as coordenadas no texto da resposta (ex: "latitude -23.55")
            lat_match = re.search(r"latitude\s+(-?\d+\.?\d*)", response_text)
            lon_match = re.search(r"longitude\s+(-?\d+\.?\d*)", response_text)

            if lat_match and lon_match:
                found_lat = float(lat_match.group(1))
                found_lon = float(lon_match.group(1))
                
                if abs(found_lat - expected_lat) > 0.01 or abs(found_lon - expected_lon) > 0.01:
                    logger.error(f"Validação falhou: Resposta cita coord ({found_lat}, {found_lon}) mas o sistema buscou ({expected_lat}, {expected_lon}).")
                    return False
            else:
                logger.warning("Coordenadas não encontradas no texto da resposta para validação.")

        # --- VALIDAÇÃO DE DADOS EXISTENTE ---
        for previsao in forecast_list:
            data = str(previsao.get("data", ""))
            max_temp = str(previsao.get("temp_max_celsius", ""))
            min_temp = str(previsao.get("temp_min_celsius", ""))
            rain = str(previsao.get("precipitacao_mm", ""))

            if data not in response_text:
                logger.error(f"Validação falhou: Data {data} não encontrada.")
                return False

            if max_temp not in response_text:
                logger.error(f"Validação falhou: Temperatura máxima {max_temp} inconsistente.")
                return False

            if min_temp not in response_text:
                logger.error(f"Validação falhou: Temperatura mínima {min_temp} inconsistente.")
                return False

            if rain not in response_text:
                logger.error(f"Validação falhou: Precipitação {rain} não encontrada.")
                return False

        logger.info("Validação concluída: Integridade total confirmada.")
        return True

    except Exception as e:
        logger.error(f"Erro crítico no validador: {e}")
        return False