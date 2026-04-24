from abc import ABC, abstractmethod


class Tool(ABC):
    name: str

    @abstractmethod
    def execute(self, topic: str) -> list[dict]:
        ...

    @abstractmethod
    def build_articles(self, data: list[dict]) -> list[dict]:
        # retorna lista de {"title": ..., "url": ..., "source": ...}
        ...
