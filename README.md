# 🌦️ Agente LLM de Previsão do Tempo

> Agente de IA para consulta de previsões meteorológicas em tempo real, utilizando **Llama 3.2:1b** via Ollama e a **API Open-Meteo** — com validação de integridade e mecanismos de fallback para máxima confiabilidade.

---

## 🚀 Destaques da Solução

| Feature                    | Descrição                                                                                                  |
| -------------------------- | ---------------------------------------------------------------------------------------------------------- |
| 🤖 **Hybrid Intelligence** | Combina a flexibilidade do LLM com precisão de Regex e extração determinística via histórico               |
| 🛡️ **Data Integrity**      | Módulo validador que garante que os dados exibidos condizem exatamente com a API (prevenção de alucinação) |
| 🔒 **Gatekeeper Security** | Filtro de entrada que evita chamadas desnecessárias ao modelo para inputs inválidos                        |
| 🧠 **Contextual Memory**   | Responde perguntas de acompanhamento recuperando coordenadas do histórico de chat                          |
| 🖥️ **UI Pronta**           | Interface amigável construída com **Gradio**                                                               |

---

## 📂 Estrutura do Projeto

```
AGENTE/
├── agent/                  # 🧠 Núcleo de inteligência
│   ├── llm_client.py       # Configuração do cliente Ollama
│   ├── tools_config.py     # Definição das tools (Function Calling)
│   └── validator.py        # Validador de integridade dos dados
├── tools/                  # 🔧 Ferramentas externas
│   └── open_meteo.py       # Integração com a API Open-Meteo
├── app.py                  # 🖥️ Interface Web (Gradio)
├── main.py                 # ⚙️ Orquestrador principal (Lógica do Agente)
├── config.py               # 🔑 Variáveis de ambiente e logs
├── requirements.txt        # 📦 Dependências do projeto
└── .gitignore              # 🙈 Proteção de arquivos
```

---

## 🛠️ Pré-requisitos

- 🐍 **Python 3.10+**
- 🦙 **Ollama** instalado e rodando
- 📥 Modelo **Llama 3.2:1b** baixado:

```bash
ollama pull llama3.2:1b
```

---

## ⚡ Instalação e Execução

**1.** Clone o repositório e acesse a pasta:

```bash
cd agente
```

**2.** Crie e ative um ambiente virtual:

```bash
python -m venv venv

# No Windows:
.\venv\Scripts\activate

# No Linux/macOS:
source venv/bin/activate
```

**3.** Instale as dependências:

```bash
pip install -r requirements.txt
```

**4.** Execute a interface de Chat:

```bash
python app.py
```

Acesse o link gerado no seu navegador — ex: [`http://127.0.0.1:7860`](http://127.0.0.1:7860)

---

## 🧠 Lógica de Funcionamento

O agente opera em **quatro camadas de segurança** para garantir que o usuário nunca fique sem resposta:

```
┌─────────────────────────────────────────────────────────┐
│  1. 🔒 GATEKEEPER      → Valida o input antes do LLM    │
│  2. 🤖 LLM TOOL CALL   → Extrai lat/lon via Function    │
│                           Calling nativo do Llama        │
│  3. 🔄 FALLBACK        → Regex + histórico recuperam     │
│                           coordenadas caso LLM alucine   │
│  4. ✅ VALIDAÇÃO FINAL  → Cruza resposta com JSON da API │
└─────────────────────────────────────────────────────────┘
```

---

## 📝 Exemplos de Execução

### ✅ Sucesso com Fallback

```
👤 Usuário: "Qual a previsão para -23.55 -46.63?"

📋 Logs:
  → LLM identificou a necessidade da TOOL...
  → Coordenadas recuperadas via Fallback...
  → Validação concluída: Integridade total confirmada.
```

### 🔁 Memória de Contexto

```
👤 Usuário: "E para os próximos dias?"

🤖 Agente: Identifica ausência de novas coordenadas,
           busca no histórico o último local consultado
           e retorna os próximos 3 dias de previsão.
```

---

## 📊 Tecnologias Utilizadas

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-Llama_3.2-000000?style=for-the-badge&logo=llama&logoColor=white)
![Gradio](https://img.shields.io/badge/Gradio-UI-FF7C00?style=for-the-badge&logo=gradio&logoColor=white)
![OpenMeteo](https://img.shields.io/badge/Open--Meteo-API-00BFFF?style=for-the-badge&logo=cloud&logoColor=white)

| Componente           | Tecnologia                   |
| -------------------- | ---------------------------- |
| 🐍 Linguagem         | Python                       |
| 🦙 LLM               | Ollama — Llama 3.2:1b        |
| 🖥️ Interface         | Gradio                       |
| 🌐 API Meteorológica | Open-Meteo (Previsão Diária) |
| 📋 Logs              | Logging nativo do Python     |

---

## 👨‍💻 Autor

Desenvolvido por **João Vitor Gomes dos Santos** — Março de 2026

---

_Obrigado pela oportinidade de mostrar um pouco do meu trabalho!_
