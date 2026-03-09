from datetime import datetime

from src.core.controllers.news import NewsController
from src.core.dto import SiteDTO
from src.core.factories.dto import NewsScrapingConfigDTO


class NewsControllerFactory:
    def __init__(
        self,
        site_dto: SiteDTO,
        config: NewsScrapingConfigDTO,
        until_date: datetime | None = None,
        session_id: int | None = None,
    ) -> None:
        self._site_dto = site_dto
        self._config = config
        self._until_date = until_date
        self._session_id = session_id

    def create(self) -> NewsController:
        return NewsController(
            url=self._site_dto.url,
            profile_id=self._site_dto.browser_provider.profile_id
            if self._site_dto.browser_provider
            else None,
            folder_id=self._site_dto.browser_provider.folder_id
            if self._site_dto.browser_provider
            else None,
            provider=self._config.provider,
            client=self._config.client,
            scraper=self._config.scraper,
            parser=self._config.parser,
            pagination=self._config.pagination,
            repository=self._config.repository,
            until_date=self._until_date,
            timezone=self._site_dto.timezone,
            site_id=self._site_dto.id,
            session_id=self._session_id,
        )
