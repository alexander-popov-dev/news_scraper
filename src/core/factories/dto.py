import inspect
from dataclasses import dataclass, field
from functools import partial
from typing import Callable

from src.core.abstract.parsers import BaseArticleParser, BaseNewsParser
from src.core.abstract.repositories import BaseArticleRepository
from src.core.abstract.scrapers import BaseScraper
from src.core.clients.abstract import BaseBrowserClient, BaseClient
from src.core.enums import CeleryQueue
from src.core.pagination.abstract import BasePagination
from src.core.providers.abstract import BaseBrowserProvider


def _is_browser_client(client_factory: Callable) -> bool:
    cls = client_factory.func if isinstance(client_factory, partial) else client_factory
    return inspect.isclass(cls) and issubclass(cls, BaseBrowserClient)


@dataclass
class NewsScrapingConfigDTO:
    scraper: type[BaseScraper]
    parser: type[BaseNewsParser]
    client: Callable[..., BaseClient]
    repository: type[BaseArticleRepository]
    pagination: Callable[..., BasePagination]
    provider: type[BaseBrowserProvider] | None = None
    queue: CeleryQueue = field(init=False)

    def __post_init__(self):
        self.queue = (
            CeleryQueue.BROWSER_SCRAPING_QUEUE
            if _is_browser_client(self.client)
            else CeleryQueue.REQUEST_SCRAPING_QUEUE
        )


@dataclass
class ArticleScrapingConfigDTO:
    scraper: type[BaseScraper]
    parser: type[BaseArticleParser]
    client: Callable[..., BaseClient]
    repository: type[BaseArticleRepository]
    provider: type[BaseBrowserProvider] | None = None
    queue: CeleryQueue = field(init=False)

    def __post_init__(self):
        self.queue = (
            CeleryQueue.BROWSER_SCRAPING_QUEUE
            if _is_browser_client(self.client)
            else CeleryQueue.REQUEST_SCRAPING_QUEUE
        )


@dataclass
class ScrapingConfigsDTO:
    news: NewsScrapingConfigDTO | None = None
    article: ArticleScrapingConfigDTO | None = None
