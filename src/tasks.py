import logging
import traceback
from datetime import datetime, timezone

from src.core.config_loader import ConfigLoader
from src.core.enums import CeleryQueue, SessionStatus, ScrapingDataType
from src.core.factories.news import NewsControllerFactory
from celery import shared_task

from src.core.repositories.django_orm.repositories import SiteRepository, ArticleRepository, SessionRepository
from src.core.telegram import TelegramManager

logger = logging.getLogger(__name__)
configs_loader = ConfigLoader()


@shared_task(queue=CeleryQueue.MANAGE_QUEUE)
def run_scraping_process_task(site_ids: list[int] | None = None):
    session_repo = SessionRepository()
    site_repo = SiteRepository()

    sites = site_repo.get_sites_for_scraping(site_ids=site_ids)

    for site_dto in sites.sites:
        queue = configs_loader.load_configs(package=site_dto.package).news.queue

        session_id = session_repo.create_session(
            scraping_type=ScrapingDataType.NEWS
        )

        run_scraping_task.apply_async(
            kwargs={
                'site_id': site_dto.id,
                'session_id': session_id
            },
            queue=queue
        )


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_kwargs={'max_retries': 5, 'countdown': 10},
    retry_backoff=True
)
def run_scraping_task(self, site_id: int, session_id: int):
    telegram = TelegramManager()
    session_repo = SessionRepository()
    site_repo = SiteRepository()
    article_repo = ArticleRepository()

    session_repo.update_session(
        session_id=session_id,
        status=SessionStatus.RUNNING,
        retries=self.request.retries
    )

    site_dto = site_repo.get_site(site_id=site_id)

    try:
        until_date = article_repo.get_latest_published_at(site_id=site_id)

        logger.info(f'Started scraping news. Site: {site_dto.package}. Until Date: {until_date}')

        config = configs_loader.load_configs(package=site_dto.package).news
        factory = NewsControllerFactory(site_dto=site_dto, config=config, until_date=until_date, session_id=session_id)

        controller = factory.create()
        total_saved = controller.run()

        session_repo.update_session(
            session_id=session_id,
            status=SessionStatus.SUCCESS,
            total_saved=total_saved,
            retries=self.request.retries,
            finished_at=datetime.now(timezone.utc)
        )

        if total_saved:
            message = (f'<b>{site_dto.name}</b>\n'
                       f'Scraped {total_saved} new article/s')
            telegram.send_message(message=message)

        logger.info(f'Finished scraping news. Site: {site_dto.package}. Saved {total_saved} new article/s')

    except Exception as e:
        logger.error(f'Error while scraping news. Site: {site_dto.package}. Error: {e}')

        session_repo.update_session(
            session_id=session_id,
            status=SessionStatus.FAILED,
            error_msg=str(e),
            traceback_msg=traceback.format_exc(),
            retries=self.request.retries,
            finished_at=datetime.now(timezone.utc)
        )

        raise
