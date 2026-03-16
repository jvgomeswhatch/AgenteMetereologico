import re
import gradio as gr

from main import run_agent
from config import logger


def is_valid_input(text: str) -> bool:

    if not isinstance(text, str):
        return False

    text = text.strip()

    has_numbers = any(char.isdigit() for char in text)

    follow_up_words = ["próximos", "dias", "continua", "mais"]

    if has_numbers:
        return True

    if any(word in text.lower() for word in follow_up_words):
        return True

    if len(text) < 3:
        return False

    return False


def handle_message(message, history):

    if history is None:
        history = []

    logger.info(f"History recebido: {history}")

    if not isinstance(message, str):
        message = str(message)

    logger.info(f"Mensagem recebida no chat: {message}")

    try:

        # --- GATEKEEPER DE ENTRADA ---

        if not is_valid_input(message):

            logger.warning(f"Entrada bloqueada pelo gatekeeper: {message}")

            return "Por favor, informe latitude e longitude (ex: -23.55 -46.63)."

        result = run_agent(message, history)

        if result.get("status") == "sucesso":

            return result.get("resposta")

        logger.warning(
            f"Entrada inválida ou fora de contexto: {message}"
        )

        return result.get(
            "mensagem",
            "Não consegui processar sua solicitação."
        )

    except Exception as e:

        logger.error(f"Erro na interface: {e}")

        return "Erro interno no agente."


def launch():

    demo = gr.ChatInterface(
        fn=handle_message,
        title="Agente de Previsão do Tempo | Desafio Técnico ClimaTempo 2026",
        description="Informe latitude e longitude | Exemplo: -23.55 -46.63. O chat responde apenas a previsão dos próximos 3 dias para a localização informada."
    )

    demo.launch(
        debug=True,
        show_error=True
    )

if __name__ == "__main__":
    launch()