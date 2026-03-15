# Agente LLM com Tool de Previsão do Tempo (Open-Meteo)

## Descrição

Este projeto implementa um **agente de IA simples** que utiliza um **LLM local via Ollama** integrado a uma **tool de previsão do tempo** baseada na API pública **Open-Meteo**.

O agente recebe uma mensagem do usuário contendo **latitude e longitude**, consulta a API meteorológica e retorna uma resposta formatada contendo:

- data da previsão
- temperatura máxima
- temperatura mínima
- precipitação diária

O sistema também inclui:

- extração automática de coordenadas da mensagem
- memória simples de conversa (histórico)
- validação de integridade entre resposta e dados da API
- tratamento básico de erros
- interface de chat utilizando **Gradio**

---

# Estrutura do Projeto

```text
agente/
│
├── app.py                # Interface de chat com Gradio
├── main.py               # Lógica principal do agente
├── config.py             # Configurações e logger
│
├── agent/
│   ├── llm_client.py     # Cliente de conexão com Ollama
│   ├── tools_config.py   # Definição das tools para o LLM
│   └── validator.py      # Validação de integridade da resposta
│
├── tools/
│   └── open_meteo.py     # Tool que consulta a API Open-Meteo
│
├── requirements.txt
└── README.md
```

---

# Dependências

O projeto utiliza **Python 3.9+**.

Principais bibliotecas:

- gradio
- requests
- openai (compatível com Ollama)

---

# Configuração do Ambiente Virtual (.venv)

Recomenda-se executar o projeto dentro de um **ambiente virtual Python (.venv)** para evitar conflitos de dependências.

## 1. Criar o ambiente virtual

No diretório do projeto:

```bash
python -m venv .venv
```

## 2. Ativar o ambiente virtual

### Windows (PowerShell)

```bash
.venv\Scripts\activate
```

### Linux / MacOS

```bash
source .venv/bin/activate
```

Após ativar o ambiente virtual, o terminal deverá mostrar algo como:

```bash
(.venv)
```

---

# Instalação das Dependências

Com o ambiente virtual ativado:

```bash
pip install -r requirements.txt
```

Exemplo de `requirements.txt`:

```text
gradio
requests
openai
```

---

# Configuração do Ollama

Este projeto utiliza um **LLM local via Ollama**.

## Instalar Ollama

https://ollama.com

## Baixar o modelo utilizado

```bash
ollama pull llama3.2:1b
```

## Iniciar o servidor Ollama

```bash
ollama serve
```

O servidor rodará por padrão em:

```
http://localhost:11434
```

---

# Como Executar o Projeto

## 1. Executar testes do agente

Rodar o arquivo principal:

```bash
python main.py
```

Esse script executa dois testes:

- consulta com coordenadas
- continuação da conversa utilizando histórico

---

## 2. Executar a interface de chat

Rodar:

```bash
python app.py
```

Abrir no navegador:

```
http://127.0.0.1:7860
```

A interface permitirá enviar mensagens e receber previsões meteorológicas.

---

# Validação da Execução

O sistema possui uma etapa de **validação de integridade dos dados**, verificando se os valores presentes na resposta formatada são consistentes com os dados retornados pela API.

Logs esperados no terminal:

```
Iniciando validação da integridade dos dados na resposta.
Validação concluída: Todos os dados do chunk estão presentes na resposta.
```

Isso garante que:

- datas
- temperaturas
- precipitação

foram corretamente incluídas na resposta final.

---

# Exemplos de Uso

## Entrada válida

```
Qual a previsão para -23.55 -46.63?
```

Resposta:

```
Previsão do tempo para latitude -23.55 e longitude -46.63:

2026-03-15 | Temperatura máxima: 30.4°C | Temperatura mínima: 18.4°C | Precipitação: 1.0 mm
2026-03-16 | Temperatura máxima: 31.0°C | Temperatura mínima: 20.5°C | Precipitação: 0.0 mm
2026-03-17 | Temperatura máxima: 30.2°C | Temperatura mínima: 19.6°C | Precipitação: 0.0 mm
```

---

## Continuação da conversa

Entrada:

```
e para os próximos dias?
```

Resposta:

```
2026-03-18 | Temperatura máxima: 30.6°C | Temperatura mínima: 16.7°C | Precipitação: 0.0 mm
2026-03-19 | Temperatura máxima: 28.5°C | Temperatura mínima: 17.7°C | Precipitação: 0.0 mm
2026-03-20 | Temperatura máxima: 29.7°C | Temperatura mínima: 17.6°C | Precipitação: 0.0 mm
```

---

## Entrada inválida

Entrada:

```
Qual a previsão para São Paulo?
```

Resposta:

```
não posso ajudar com isso. Por favor Insira a a longitudade e latidude para obter a previsão.
```

---

# Funcionalidades Implementadas

- Integração com **LLM local via Ollama**
- Function calling / tools
- Consulta à API **Open-Meteo**
- Extração automática de coordenadas
- Memória simples de conversa
- Paginação de previsões
- Validação de integridade dos dados
- Interface de chat com **Gradio**
- Tratamento básico de erros e logs

---

# João Vitor Gomes dos Santos

Projeto desenvolvido como **desafio técnico para implementação de um agente LLM com integração de tools externas**.
