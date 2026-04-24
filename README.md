# news-digest-agent

Agente de notícias multi-step rodando 100% local com [Ollama](https://ollama.com/). Dado um pedido em português, o sistema orquestra quatro agentes em sequência para buscar, filtrar e resumir notícias de fontes públicas.

---

## Arquitetura

```
Você: "me resumo as notícias de inteligência artificial hoje"
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│ 1. PLANNER                                                  │
│    Entrada : texto livre do usuário                         │
│    Faz     : LLM decide quais fontes usar + traduz tópico   │
│    Saída   : {"tools": ["get_hackernews"], "topic": "AI"}   │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. EXECUTOR                                                 │
│    Entrada : lista de tool names + tópico                   │
│    Faz     : chama cada API e coleta artigos brutos         │
│    Saída   : lista de {title, url, source}                  │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. CRITIC                                                   │
│    Entrada : todos os artigos coletados                     │
│    Faz     : LLM avalia relevância e seleciona os melhores  │
│    Saída   : [0, 3, 5]  ← índices dos artigos escolhidos    │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. RESPONDER                                                │
│    Entrada : artigos filtrados + pedido original            │
│    Faz     : LLM gera digest em português com links         │
│    Saída   : texto formatado em bullets para o usuário      │
└─────────────────────────────────────────────────────────────┘
```

---

## O que cada agente faz e por que existe

### Planner — `core/planner.py`
O usuário escreve em português e pode pedir qualquer coisa. O planner usa o LLM para:
- Entender a intenção e extrair o tema
- Traduzir o tópico para inglês (as APIs são em inglês)
- Decidir quais das 3 fontes fazem sentido para o pedido

Retorna JSON estruturado:
```json
{"tools": ["get_hackernews", "get_devto"], "topic": "artificial intelligence"}
```

Sem o planner, seria necessário keyword matching manual — como no `clima-local`.

---

### Executor — `core/executor.py`
Recebe a lista de tools do planner e as executa em sequência. Cada tool:
1. Chama sua API
2. Normaliza o resultado para `{"title", "url", "source"}`

É genérico — não sabe o que cada tool faz, só delega.

---

### Critic — `core/critic.py`
Recebe todos os artigos brutos (pode ser 15+) e usa o LLM para julgar relevância. Monta uma lista numerada e pede ao modelo:

```
0. [HackerNews] OpenAI announces new model
1. [Reddit] Best Python libraries 2024
2. [Dev.to] Getting started with AI agents
...
```

O modelo retorna só os índices mais relevantes: `[0, 2, 5]`

Sem o critic, o responder receberia muito ruído e geraria um resumo fraco.

---

### Responder — `core/responder.py`
Recebe apenas os artigos já filtrados e gera o digest final em português. É o único agente focado exclusivamente em qualidade de escrita — os outros agentes já trataram de relevância e filtragem.

---

## Prompts usados em cada etapa

### Prompt do Planner
```
Você é um planejador de busca de notícias.
Fontes disponíveis: get_hackernews, get_reddit, get_devto
Com base no pedido, decida quais fontes usar e extraia o tópico em inglês.
Retorne APENAS JSON.
Exemplo: {"tools": ["get_hackernews"], "topic": "artificial intelligence"}
Pedido: {user_input}
```

### Prompt do Critic
```
Você é um editor crítico de notícias.
Filtre a lista e selecione os 5 mais relevantes para o tópico "{topic}".
Retorne APENAS um JSON array com os índices. Exemplo: [0, 2, 4]

ARTIGOS:
0. [HackerNews] título...
1. [Reddit] título...
```

### Prompt do Responder
```
Gere um digest de notícias conciso em português sobre "{topic}".
Use bullets (•), máximo 8 linhas. Para cada artigo inclua título e link.

ARTIGOS SELECIONADOS:
- título (fonte) — url
```

---

## Fontes (sem autenticação)

| Tool | API | O que busca |
|------|-----|-------------|
| `get_hackernews` | [HackerNews Firebase](https://github.com/HackerNews/API) | Top stories do dia |
| `get_reddit` | Reddit `.json` | Posts em alta no subreddit do tema |
| `get_devto` | [Dev.to API](https://developers.forem.com/api) | Artigos por tag |

---

## Setup

```bash
# instale o modelo
ollama pull qwen2.5:7b

# clone e rode
git clone https://github.com/Dowingows/news-digest-agent.git
cd news-digest-agent
pip install requests
python main.py
```

### Modo debug (mostra os prompts de cada etapa)
```bash
DEBUG=1 python main.py
```

---

## Estrutura

```
news-digest-agent/
├── main.py              # pipeline: plan → execute → critic → respond
├── config.py            # modelo, URLs, limites
├── core/
│   ├── planner.py       # agente 1: LLM → JSON com tools e tópico
│   ├── executor.py      # agente 2: roda as tools, coleta artigos
│   ├── critic.py        # agente 3: LLM → filtra por relevância
│   ├── responder.py     # agente 4: LLM → digest final
│   └── llm.py           # wrapper do Ollama
└── tools/
    ├── hackernews.py
    ├── reddit.py
    └── devto.py
```

---

> Projeto de aprendizado — foco em entender como múltiplos agentes LLM se encadeiam numa pipeline real.
