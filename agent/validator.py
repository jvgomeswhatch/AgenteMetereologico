import logging

logger = logging.getLogger(__name__)

def validate_forecast(response_text: str, forecast_list: list) -> bool:
    """
    Verifica se os valores exibidos na resposta final correspondem
    aos valores da lista de previsões processada.

    Args:
        response_text (str): texto final enviado ao usuário (resposta formatada)
        forecast_list (list): lista de dicionários contendo os dados da previsão
    """

    if not forecast_list:
        logger.warning("Validador recebeu uma lista de previsão vazia.")
        return False

    try:
        logger.info("Iniciando validação da integridade dos dados na resposta.")

        for previsao in forecast_list:
            # Extraímos os valores exatamente como foram processados no main.py
            data = str(previsao.get("data", ""))
            max_temp = str(previsao.get("temp_max_celsius", ""))
            min_temp = str(previsao.get("temp_min_celsius", ""))
            rain = str(previsao.get("precipitacao_mm", ""))

            # Validação: Verifica se cada dado importante aparece no texto final
            if data not in response_text:
                logger.error(f"Validação falhou: Data {data} não encontrada na resposta.")
                return False

            if max_temp not in response_text:
                logger.error(f"Validação falhou: Temperatura máxima {max_temp} inconsistente para {data}.")
                return False

            if min_temp not in response_text:
                logger.error(f"Validação falhou: Temperatura mínima {min_temp} inconsistente para {data}.")
                return False

            if rain not in response_text:
                logger.error(f"Validação falhou: Precipitação {rain} não encontrada para a data {data}.")
                return False

        logger.info("Validação concluída: Todos os dados do chunk estão presentes na resposta.")
        return True

    except Exception as e:
        logger.error(f"Erro crítico durante a execução do validador: {e}")
        return False