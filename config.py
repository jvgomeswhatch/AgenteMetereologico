import logging

MODEL_NAME = "llama3.2:1b"
LLM_BASE_URL = "http://localhost:11434/v1"
API_TIMEOUT_SECONDS = 10
DEFAULT_TIMEZONE = "America/Sao_Paulo"

# Configuração centralizada de Logging
# O nível INFO mostrará o fluxo normal. Em produção, você poderia mudar para WARNING ou ERROR.
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
# Criamos um logger padrão para ser importado pelos outros arquivos
logger = logging.getLogger("WeatherAgent")