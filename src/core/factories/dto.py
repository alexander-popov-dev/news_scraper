from dataclasses import dataclass
from typing import Callable

from src.core.abstract.parsers import BaseNewsParser, BaseArticleParser
from src.core.abstract.repositories import BaseArticleRepository
from src.core.abstract.scrapers import BaseScraper
from src.core.clients.abstract import BaseClient
from src.core.enums import CeleryQueue, BrowserProvider
from src.core.pagination.abstract import BasePagination
from src.core.providers.abstract import BaseBrowserProvider


@dataclass
class NewsScrapingConfigDTO:
    scraper: type[BaseScraper]
    parser: type[BaseNewsParser]
    client: type[BaseClient]
    repository: type[BaseArticleRepository]
    pagination: Callable[..., BasePagination]
    queue: CeleryQueue
    provider: type[BaseBrowserProvider] | None = None


@dataclass
class ArticleScrapingConfigDTO:
    scraper: type[BaseScraper]
    parser: type[BaseArticleParser]
    client: type[BaseClient]
    repository: type[BaseArticleRepository]
    queue: CeleryQueue
    provider: BrowserProvider | None = None

@dataclass
class ScrapingConfigsDTO:
    news: NewsScrapingConfigDTO | None = None
    article: ArticleScrapingConfigDTO | None = None