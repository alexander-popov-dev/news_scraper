from abc import ABC, abstractmethod

from src.core.dto import ArticlesDTO, ArticleDTO


class BaseNewsParser(ABC):
    @abstractmethod
    def parse_news(self, content: str, page_url: str, timezone: str | None) -> ArticlesDTO:
        pass

class BaseArticleParser(ABC):
    @abstractmethod
    def parse_article(self, content: str) -> ArticleDTO:
        pass
