from src.core.enums import CeleryQueue
from src.core.factories.dto import NewsScrapingConfigDTO, ScrapingConfigsDTO
from src.core.pagination.pagination import PagePagination
from src.core.repositories.django_orm.repositories import ArticleRepository
from .news.scraper import NewsScraper
from .news.parser import NewsParser
from ...core.clients.request.requests.client import RequestsClient
from ...core.providers.nst.provider import NstBrowser

SCRAPING_CONFIGS = ScrapingConfigsDTO(
    news=NewsScrapingConfigDTO(
        provider=NstBrowser,
        scraper=NewsScraper,
        parser=NewsParser,
        client=RequestsClient,
        repository=ArticleRepository,
        pagination=PagePagination,
        queue=CeleryQueue.REQUEST_SCRAPING_QUEUE
    )
)
