# agent/tools_config.py

weather_tool_schema = {
    "type": "function",
    "function": {
        "name": "get_daily_forecast",
        "description": (
            "Obtém a previsão do tempo diária para uma localização "
            "usando latitude e longitude."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "lat": {
                    "type": "number",
                    "description": "Latitude da localização."
                },
                "lon": {
                    "type": "number",
                    "description": "Longitude da localização."
                },
                "days_ahead": {
                    "type": "integer",
                    "description": "Número de dias à frente para a previsão (0 para hoje, 1 para amanhã, etc.).",
                    "default": 3
                }
            },

            "required": ["lat", "lon"]
        }
    }
}

tools_list = [weather_tool_schema]