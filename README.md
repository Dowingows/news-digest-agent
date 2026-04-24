# news-digest-agent

Agente multi-step que busca, filtra e resume notícias usando um pipeline **Planner → Executor → Critic → Responder** rodando 100% local com [Ollama](https://ollama.com/).

---

## O que aprende com este projeto

| Agente | Responsabilidade |
|--------|-----------------|
| **Planner** | LLM decide quais fontes usar e extrai o tópico em inglês → retorna JSON |
| **Executor** | Chama as APIs e coleta artigos brutos de cada fonte |
| **Critic** | LLM lê todos os artigos e seleciona os mais relevantes → retorna JSON de índices |
| **Responder** | LLM gera o digest final em português com links |

---

## Fluxo

```
Você: "me resumo as notícias de inteligência artificial"

[planner] tópico: artificial intelligence | fontes: get_hackernews, get_devto
[tool: get_hackernews]
[tool: get_devto]
[critic] filtrando 10 artigos...

Assistente:
• OpenAI lança novo modelo...  — https://...
• Meta anuncia mudanças...     — https://...
```

---

## Setup

```bash
ollama pull llama3.2

git clone https://github.com/Dowingows/news-digest-agent.git
cd news-digest-agent
pip install requests

python main.py
```

---

## Fontes (sem autenticação)

| Tool | API |
|------|-----|
| `get_hackernews` | [HackerNews Firebase API](https://github.com/HackerNews/API) |
| `get_reddit` | Reddit `.json` endpoints |
| `get_devto` | [Dev.to API](https://developers.forem.com/api) |

---

## Estrutura

```
news-digest-agent/
├── main.py
├── config.py
├── core/
│   ├── planner.py    # LLM → JSON com tools e tópico
│   ├── executor.py   # roda as tools, coleta artigos
│   ├── critic.py     # LLM → filtra artigos por relevância
│   ├── responder.py  # LLM → digest final
│   └── llm.py
└── tools/
    ├── hackernews.py
    ├── reddit.py
    └── devto.py
```
