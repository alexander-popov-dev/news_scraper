import logging
from urllib.parse import urlparse

from playwright.sync_api import (
    Browser,
    BrowserContext,
    Page,
    Playwright,
    sync_playwright,
)

from server.settings import HEADLESS
from src.core.clients.abstract import BaseBrowserClient

logger = logging.getLogger(__name__)


class PlaywrightClient(BaseBrowserClient):
    def __init__(
        self, proxy: str | None = None, cdp_endpoint_url: str | None = None
    ) -> None:
        self._cdp_endpoint_url: str | None = cdp_endpoint_url
        self._proxy: str | None = proxy
        self._playwright: Playwright | None = None
        self._context: BrowserContext | None = None
        self._browser: Browser | None = None
        self._page: Page | None = None
        self._storage: dict | None = None

    def _get_proxy(self) -> dict | None:
        if not self._proxy:
            return None

        parsed = urlparse(self._proxy)

        proxy = {"server": f"{parsed.scheme}://{parsed.hostname}:{parsed.port}"}

        if parsed.username:
            proxy["username"] = parsed.username

        if parsed.password:
            proxy["password"] = parsed.password

        return proxy

    def start(self) -> None:
        self._playwright = sync_playwright().start()

        if self._cdp_endpoint_url:
            self._browser = self._playwright.chromium.connect_over_cdp(
                endpoint_url=self._cdp_endpoint_url
            )
            self._context = self._browser.contexts[0]
            self._page = self._context.pages[0]
            logger.info("Playwright over CDP successfully started")

        else:
            self._browser = self._playwright.firefox.launch(headless=HEADLESS)
            self._context = self._browser.new_context()
            self._page = self._context.new_page()
            logger.info("Playwright successfully started")

    def close(self) -> None:
        if self._browser:
            self._browser.close()

        if self._playwright:
            self._playwright.stop()

        logger.info("Playwright successfully stopped")

    def get_page(self) -> Page:
        return self._page
