import logging
from abc import ABC, abstractmethod

from src.core.dto import ArticleDTO, ArticlesDTO

logger = logging.getLogger(__name__)


class BaseNewsParser(ABC):
    @abstractmethod
    def get_article_items(self, content: str) -> list: ...

    @abstractmethod
    def parse_article_item(
        self, article, page_url: str, timezone: str | None
    ) -> ArticleDTO: ...

    def parse_news(
        self, content: str, page_url: str, timezone: str | None
    ) -> ArticlesDTO:
        article_dto_list = []
        warnings = []

        for article in self.get_article_items(content):
            try:
                article_dto_list.append(
                    self.parse_article_item(article, page_url, timezone)
                )
            except Exception as e:
                msg = f"Skipping article on {page_url}: {e}"
                logger.warning(msg)
                warnings.append(msg)

        return ArticlesDTO(articles=article_dto_list, warnings=warnings)


class BaseArticleParser(ABC):
    @abstractmethod
    def parse_article(self, content: str) -> ArticleDTO:
        pass
