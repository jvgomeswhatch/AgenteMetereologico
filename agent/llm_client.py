from openai import OpenAI
from config import LLM_BASE_URL

def get_llm_client():
    """
    Inicializa e retorna o cliente LLM apontando para o servidor local do Ollama.
    """
    client = OpenAI(
        base_url='http://localhost:11434/v1', # O redirecionamento para o Ollama
        api_key='ollama', # O Ollama não exige chave real, mas a biblioteca exige uma string
    )
    
    return client