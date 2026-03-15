import gradio as gr

from main import run_agent
from config import logger


def handle_message(message, history):

    if history is None:
        history = []

    logger.info(f"History recebido: {history}")

    if not isinstance(message, str):
        message = str(message)

    logger.info(f"Mensagem recebida no chat: {message}")

    try:

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
        title="Agente de Previsão do Tempo | Desafio Técnico",
        description="Informe latitude e longitude. Exemplo: -23.55 -46.63"
    )

    demo.launch(
        debug=True,
        show_error=True
    )


if __name__ == "__main__":
    launch()