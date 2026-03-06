import logging
from datetime import datetime

from src.core.abstract.repositories import BaseArticleRepository
from src.core.clients.abstract import BaseClient
from src.core.enums import ScrapingDataType
from src.core.pagination.abstract import BasePagination
from src.core.abstract.parsers import BaseNewsParser
from src.core.abstract.scrapers import BaseScraper
from src.core.dto import ArticlesDTO
from src.core.providers.abstract import BaseBrowserProvider

logger = logging.getLogger(__name__)


class NewsController:
    def __init__(
            self,
            url: str,
            provider: type[BaseBrowserProvider],
            client: type[BaseClient],
            scraper: type[BaseScraper],
            parser: type[BaseNewsParser],
            pagination: type[BasePagination],
            repository: type[BaseArticleRepository],
            site_id: int,
            session_id: int,
            profile_id: str | None = None,
            folder_id: str | None = None,
            proxy: str | None = None,
            until_date: datetime | None = None,
            timezone: str | None = None
    ) -> None:
        self._provider = provider(profile_id=profile_id, folder_id=folder_id, close_profile=False) if provider else None
        self._client = client
        self._scraper = scraper
        self._parser = parser()
        self._pagination = pagination(url=url)
        self._repository = repository()
        self._until_date = until_date
        self._timezone = timezone
        self._site_id = site_id
        self._session_id = session_id
        self._proxy = proxy

    def run(self) -> int:
        articles = []

        with self._client(proxy=self._proxy, provider=self._provider) as client:
            scraper = self._scraper(client=client)

            for url in self._pagination:
                logger.info(f'Fetching news from {url}')

                response_dto = scraper.run(url=url)

                self._repository.save_raw_response_data(
                    response_dto=response_dto,
                    site_id=self._site_id,
                    scraping_type=ScrapingDataType.NEWS,
                    session_id=self._session_id
                )

                articles_dto = self._parser.parse_news(
                    content=response_dto.text(),
                    page_url=url,
                    timezone=self._timezone
                )
                articles.extend(articles_dto.articles)

                if not articles_dto.articles or not self._until_date:
                    self._pagination.stop()

                for article in articles_dto.articles:
                    if self._until_date and article.published_at and article.published_at <= self._until_date:
                        self._pagination.stop()
                        break

        return self._repository.save_articles(
            articles_dto=ArticlesDTO(articles=articles, site_id=self._site_id),
            scraping_type=ScrapingDataType.NEWS,
            session_id=self._session_id
        )
