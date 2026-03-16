🌦️ Agente LLM Meteorológico
Desafio Técnico de IA | ClimaTempo 2026 — Open-Meteo + Ollama
📌 Descrição

Este projeto implementa um Agente de IA para previsão do tempo utilizando modelos de linguagem locais.
A aplicação conecta o modelo Llama 3.2 1B (via Ollama) à API Open-Meteo, permitindo que um LLM consulte dados meteorológicos reais através de uma tool externa.

O sistema foi projetado com foco em confiabilidade, incluindo validações e mecanismos de fallback para reduzir erros de interpretação do modelo.

O agente recebe coordenadas geográficas (latitude e longitude) e retorna:

📅 Data da previsão

🌡️ Temperatura mínima e máxima (°C)

🌧️ Volume de precipitação (mm)

🏗️ Arquitetura do Sistema

O projeto foi estruturado de forma modular, separando claramente interface, lógica do agente e integrações externas.

agente/
│
├── app.py
│ Interface Web (Gradio) + Gatekeeper de entrada
│
├── main.py
│ Orquestrador do agente e loop de decisão
│
├── config.py
│ Configurações globais e sistema de logs
│
├── agent/
│ ├── llm_client.py
│ │ Wrapper para comunicação com Ollama
│ │
│ ├── tools_config.py
│ │ Definição das ferramentas em JSON Schema
│ │
│ └── validator.py
│ Motor de validação de dados (anti-alucinação)
│
├── tools/
│ └── open_meteo.py
│ Integração direta com a API Open-Meteo
│
└── requirements.txt
Dependências do projeto
🛠️ Tecnologias Utilizadas

Python 3.9+

Ollama — execução de LLM local

Llama 3.2 1B

Gradio — interface web

OpenAI Python SDK — interface compatível com Ollama

Requests — consumo da API REST

Open-Meteo API — dados meteorológicos

🧠 Diferenciais de Engenharia

Para melhorar a confiabilidade do agente com um modelo pequeno (1B), foram implementadas algumas camadas de proteção:

🔎 Gatekeeper de Entrada

Valida se a pergunta do usuário está relacionada a previsão do tempo antes de acionar o LLM.

🔁 Fallback Determinístico

Caso o modelo não execute corretamente a chamada da ferramenta, um extrator baseado em Regex tenta recuperar as coordenadas.

📍 Proteção de Coordenadas

Evita que o modelo arredonde ou modifique latitude/longitude fornecidas pelo usuário.

🛡️ Validação Anti-Alucinação

O módulo validator.py garante que os números exibidos ao usuário correspondem exatamente aos dados retornados pela API.

💬 Gestão de Contexto

O agente pode recuperar coordenadas mencionadas anteriormente para responder perguntas de acompanhamento.

🚀 Como Executar o Projeto
1️⃣ Criar ambiente virtual
python -m venv .venv

Ativar o ambiente:

Windows

.venv\Scripts\activate

Linux / Mac

source .venv/bin/activate
2️⃣ Instalar dependências
pip install -r requirements.txt
3️⃣ Configurar o Ollama

Instale e execute o servidor:

ollama serve

Baixe o modelo utilizado:

ollama pull llama3.2:1b
4️⃣ Executar a aplicação
python app.py

A interface ficará disponível em:

http://127.0.0.1:7860
💬 Exemplo de Uso

Pergunta do usuário:

Qual a previsão do tempo para latitude -23.30 e longitude -45.96?

Resposta esperada:

Data: 2026-03-11
Temperatura mínima: 18°C
Temperatura máxima: 27°C
Precipitação: 2.4 mm

👨‍💻 Desenvolvedor
João Vitor Gomes dos Santos
