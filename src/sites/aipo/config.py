from functools import partial

from src.core.clients.request.requests.client import RequestsClient
from src.core.factories.dto import NewsScrapingConfigDTO, ScrapingConfigsDTO
from src.core.pagination.pagination import OffsetPagination
from src.core.repositories.django_orm.repositories import ArticleRepository

from .news.parser import NewsParser
from .news.scraper import NewsScraper

SCRAPING_CONFIGS = ScrapingConfigsDTO(
    news=NewsScrapingConfigDTO(
        scraper=NewsScraper,
        parser=NewsParser,
        client=RequestsClient,
        repository=ArticleRepository,
        pagination=partial(OffsetPagination, start_offset=0, step=9),
    )
)
