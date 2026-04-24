from core.planner import plan
from core.executor import execute
from core.critic import filter_articles
from core.responder import respond


def main():
    print("News Digest Agent. Digite 'sair' para encerrar.\n")
    while True:
        try:
            user_input = input("Você: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nAté logo!")
            break

        if not user_input:
            continue
        if user_input.lower() in ["sair", "exit", "quit"]:
            print("Até logo!")
            break

        result     = plan(user_input)
        topic      = result["topic"]
        tool_names = result["tools"]

        print(f"[planner] tópico: {topic} | fontes: {', '.join(tool_names)}")

        articles = execute(tool_names, topic)
        if not articles:
            print("Assistente: Não encontrei artigos sobre esse tema.\n")
            continue

        print(f"[critic] filtrando {len(articles)} artigos...")
        filtered = filter_articles(articles, topic)

        digest = respond(user_input, topic, filtered)
        print(f"\nAssistente:\n{digest}\n")


if __name__ == "__main__":
    main()
