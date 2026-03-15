import requests
from config import logger, API_TIMEOUT_SECONDS, DEFAULT_TIMEZONE

def get_daily_forecast(lat: float, lon: float, days_ahead: int = 3) -> dict:
    """
    Busca a previsão do tempo diária no Open-Meteo com validação rigorosa.
    """
    logger.info(f"Iniciando busca de previsão para lat:{lat}, lon:{lon}, dias:{days_ahead}")
    
    # 1. Validação explícita de parâmetros (Fail Fast)
    if not (-90.0 <= lat <= 90.0):
        logger.warning(f"Latitude inválida recebida: {lat}")
        return {"status": "erro", "mensagem": "A latitude deve estar entre -90 e 90."}
    
    if not (-180.0 <= lon <= 180.0):
        logger.warning(f"Longitude inválida recebida: {lon}")
        return {"status": "erro", "mensagem": "A longitude deve estar entre -180 e 180."}
        
    if days_ahead <= 0:
        logger.warning(f"Número de dias inválido: {days_ahead}")
        return {"status": "erro", "mensagem": "O número de dias deve ser maior que zero."}

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_sum"],
        "timezone": DEFAULT_TIMEZONE,
        "forecast_days": days_ahead
    }

    try:
        response = requests.get(url, params=params, timeout=API_TIMEOUT_SECONDS)
        response.raise_for_status()
        
        data = response.json()
        daily_data = data.get("daily", {})
        times = daily_data.get("time", [])
        temp_max = daily_data.get("temperature_2m_max", [])
        temp_min = daily_data.get("temperature_2m_min", [])
        precip = daily_data.get("precipitation_sum", [])
        
        # 2. Tratamento seguro de dados da API (Garantindo que os arrays têm o mesmo tamanho)
        if not (len(times) == len(temp_max) == len(temp_min) == len(precip)):
            logger.error("Inconsistência nos dados retornados pela API Open-Meteo.")
            return {"status": "erro", "mensagem": "Falha na formatação dos dados da API."}

        formatted_forecast = []
        for i in range(len(times)):
            formatted_forecast.append({
                "data": times[i],
                "temp_max_celsius": temp_max[i],
                "temp_min_celsius": temp_min[i],
                "precipitacao_mm": precip[i]
            })
            
        logger.info("Previsão do tempo obtida e formatada com sucesso.")
        return {
            "status": "sucesso",
            "previsao": formatted_forecast
        }
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Falha de conexão com a API: {str(e)}")
        return {
            "status": "erro",
            "mensagem": "Serviço meteorológico temporariamente indisponível."
        }
    



    