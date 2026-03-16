Agente LLM Meteorológico | Desafio ClimaTempo (Open-Meteo + Ollama)
📋 Descrição
Este projeto apresenta um Agente de IA Resiliente capaz de fornecer previsões meteorológicas precisas utilizando modelos de linguagem locais. A solução conecta o Llama 3.2 1B (via Ollama) à API Open-Meteo, focando em estabilidade e integridade de dados através de camadas de validação e fallbacks determinísticos.

O agente processa coordenadas geográficas (Latitude e Longitude) e retorna:

📅 Data da previsão

🌡️ Temperatura Máxima e Mínima (°C)

🌧️ Volume de Precipitação (mm)

🏗️ Arquitetura do Sistema
O projeto foi desenvolvido seguindo princípios de modularização para facilitar a manutenção e testes independentes.

Plaintext
agente/
│
├── app.py # Interface Web (Gradio) e lógica de Gatekeeper
├── main.py # Orquestrador do Agente e Loop de Decisão
├── config.py # Configurações globais e Logs
│
├── agent/
│ ├── llm_client.py # Wrapper para comunicação com Ollama
│ ├── tools_config.py # Definição técnica das ferramentas (JSON Schema)
│ └── validator.py # Motor de consistência de dados (Anti-Alucinação)
│
├── tools/
│ └── open_meteo.py # Integração direta com a API Open-Meteo
│
└── requirements.txt # Dependências do projeto
🛠️ Tecnologias Utilizadas
Python 3.9+

Ollama (Hospedagem de LLM Local)

Gradio (Interface de Usuário)

OpenAI Python SDK (Interface compatível com o Ollama)

Requests (Consumo de API REST)

🧠 Diferenciais de Engenharia (Camadas de Segurança)
Para superar as limitações de modelos locais pequenos, foram implementadas as seguintes estratégias:

Gatekeeper de Entrada: Filtro preventivo no app.py que valida se o input do usuário possui potencial meteorológico antes de consumir recursos do LLM.

Fallback Determinístico (Regex): Caso o LLM não consiga formatar a chamada de função (Tool Call) corretamente, o sistema aciona um extrator via Expressão Regular para garantir que a previsão seja entregue.

Proteção de Coordenadas: O agente verifica se o LLM tentou "inventar" ou alterar as coordenadas fornecidas pelo usuário (proteção contra alucinação geográfica).

Módulo de Validação (Validator): Uma verificação pós-processamento que garante que os números exibidos no chat são exatamente os mesmos retornados pela API.

Gestão de Contexto (Histórico): Recuperação inteligente de coordenadas de mensagens anteriores, permitindo perguntas como "e para os próximos dias?" sem repetição de dados.

🚀 Como Executar

1. Preparação do Ambiente
   Bash

# Criar ambiente virtual

python -m venv .venv

# Ativar ambiente (Windows)

.venv\Scripts\activate

# Instalar dependências

pip install -r requirements.txt 2. Configuração do LLM (Ollama)
Certifique-se de que o Ollama está rodando e o modelo instalado:

Bash
ollama pull llama3.2:1b
ollama serve 3. Inicialização
Para testes em terminal:

Bash
python main.py
Para interface visual (Gradio):

Bash
python app.py
Acesse em: http://127.0.0.1:7860

📊 Exemplos de Execução (Logs de Resiliência)
O sistema registra cada etapa da tomada de decisão:

Identificação de Tool: INFO - LLM identificou a necessidade da TOOL com sucesso.

Recuperação de Memória: INFO - Coordenadas recuperadas do HISTÓRICO: lat=-23.55, lon=-46.63

Validação: INFO - Validação concluída: Todos os dados do chunk estão presentes na resposta.

👤 Desenvolvedor
João Vitor Gomes dos Santos
Desafio Técnico: Implementação de Agentes com Local LLMs e Function Calling.
