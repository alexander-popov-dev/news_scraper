from datetime import datetime

from django.db.models import Prefetch

from src.core.abstract.repositories import BaseArticleRepository, BaseSiteRepository, BaseSessionRepository
from src.core.dto import ArticleDTO, ArticlesDTO, SiteDTO, SitesDTO, ResponseDTO, BrowserProviderDTO
from src.core.enums import ScrapingDataType, SessionStatus
from src.models import Article, Site, RawResponseData, Session, BrowserProfile


class ArticleRepository(BaseArticleRepository):
    def save_articles(
            self,
            articles_dto: ArticlesDTO,
            scraping_type: ScrapingDataType,
            session_id: int
    ) -> list[ArticleDTO]:
        urls = [article.url for article in articles_dto.articles]

        existing_urls = set(
            Article.objects
            .filter(url__in=urls)
            .values_list('url', flat=True)
        )

        new_articles = [
            Article(
                url=article.url,
                title=article.title,
                subtitle=article.subtitle,
                published_at=article.published_at,
                site_id=articles_dto.site_id,
                scraping_type=scraping_type,
                session_id=session_id
            )
            for article in articles_dto.articles
            if article.url not in existing_urls
        ]

        if not new_articles:
            return []

        Article.objects.bulk_create(new_articles)

        return [
            ArticleDTO(url=a.url, title=a.title, subtitle=a.subtitle, published_at=a.published_at)
            for a in new_articles
        ]

    def get_latest_published_at(self, site_id: int) -> datetime | None:
        return (
            Article.objects
            .filter(site_id=site_id)
            .order_by('-published_at')
            .values_list('published_at', flat=True)
            .first()
        )

    def save_raw_response_data(
            self,
            response_dto: ResponseDTO,
            site_id: int,
            scraping_type: ScrapingDataType,
            session_id: int
    ) -> None:
        RawResponseData.objects.create(
            site_id=site_id,
            session_id=session_id,
            url=response_dto.url,
            scraping_type=scraping_type,
            request_data=response_dto.request_info,
            response_text=response_dto.text()
        )


class SiteRepository(BaseSiteRepository):
    def get_site(self, site_id: int) -> SiteDTO | None:
        site = (
            Site.objects
            .filter(pk=site_id)
            .prefetch_related(
                Prefetch(
                    'browser_profiles',
                    queryset=BrowserProfile.objects.filter(is_active=True),
                    to_attr='active_profiles',
                )
            )
            .first()
        )

        if not site:
            return None

        profile = next(iter(site.active_profiles), None)

        browser_provider = (
            BrowserProviderDTO(
                id=profile.pk,
                site_id=site.pk,
                provider=profile.provider,
                is_active=profile.is_active,
                profile_id=profile.profile_id,
                folder_id=profile.folder_id,
            )
            if profile
            else None
        )

        return SiteDTO(
            id=site.pk,
            url=site.url,
            name=site.name,
            proxy=site.proxy,
            package=site.package,
            timezone=site.timezone,
            is_active=site.is_active,
            browser_provider=browser_provider,
        )

    def get_sites_for_scraping(self, site_ids: list[int] | None = None) -> SitesDTO | None:
        if site_ids:
            queryset = Site.objects.filter(pk__in=site_ids)
        else:
            queryset = Site.objects.filter(is_active=True)

        queryset = queryset.prefetch_related(
            Prefetch(
                'browser_profiles',
                queryset=BrowserProfile.objects.filter(is_active=True),
                to_attr='active_profiles',
            )
        )

        site_dto_list = [
            SiteDTO(
                id=site.pk,
                url=site.url,
                name=site.name,
                proxy=site.proxy,
                package=site.package,
                timezone=site.timezone,
                is_active=site.is_active,
                browser_provider=(
                    BrowserProviderDTO(
                        id=profile.pk,
                        site_id=site.pk,
                        provider=profile.provider,
                        is_active=profile.is_active,
                        profile_id=profile.profile_id,
                        folder_id=profile.folder_id,
                    )
                    if (profile := next(iter(site.active_profiles), None))
                    else None
                ),
            )
            for site in queryset
        ]

        return SitesDTO(sites=site_dto_list)


class SessionRepository(BaseSessionRepository):
    def create_session(self, scraping_type: ScrapingDataType) -> int:
        session = Session.objects.create(status=SessionStatus.CREATED, scraping_type=scraping_type)
        return session.pk

    def update_session(
            self,
            session_id: int,
            status: SessionStatus,
            error_msg: str | None = None,
            traceback_msg: str | None = None,
            total_saved: int = 0,
            retries: int = 0,
            finished_at: datetime | None = None
    ) -> None:
        Session.objects.filter(id=session_id).update(
            status=status,
            error_msg=error_msg,
            traceback_msg=traceback_msg,
            total_saved=total_saved,
            retries=retries,
            finished_at=finished_at
        )
