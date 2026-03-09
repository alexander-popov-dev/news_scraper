from abc import ABC, abstractmethod
from datetime import datetime
from src.core.dto import ArticleDTO, ArticlesDTO, SitesDTO, SiteDTO, ResponseDTO
from src.core.enums import ScrapingDataType, SessionStatus


class BaseArticleRepository(ABC):
    @abstractmethod
    def save_articles(self, articles_dto: ArticlesDTO, scraping_type: ScrapingDataType, session_id: int) -> list[ArticleDTO]:
        ...

    @abstractmethod
    def get_latest_published_at(self, site_id: int) -> datetime | None:
        ...

    @abstractmethod
    def save_raw_response_data(
            self,
            response_dto: ResponseDTO,
            site_id: int,
            scraping_type: ScrapingDataType,
            session_id: int
    ) -> None:
        ...


class BaseSiteRepository(ABC):
    @abstractmethod
    def get_sites_for_scraping(self, site_ids: list[int] | None = None) -> SitesDTO | None:
        ...

    @abstractmethod
    def get_site(self, site_id: int) -> SiteDTO | None:
        ...


class BaseSessionRepository(ABC):
    @abstractmethod
    def create_session(self, scraping_type: ScrapingDataType) -> int:
        ...

    @abstractmethod
    def update_session(
            self,
            session_id: int,
            status: SessionStatus,
            error_msg: str | None = None,
            traceback_msg: str | None = None,
            total_saved: int = 0,
            retries: int = 0,
            finished_at: datetime | None = None,
    ) -> None:
        ...