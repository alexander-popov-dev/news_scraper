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
from src.core.providers.abstract import BaseBrowserProvider

logger = logging.getLogger(__name__)


class PlaywrightClient(BaseBrowserClient):
    def __init__(
        self,
        proxy: str | dict | None = None,
        provider: BaseBrowserProvider | None = None,
    ) -> None:
        self._playwright: Playwright | None = None
        self._context: BrowserContext | None = None
        self._browser: Browser | None = None
        self._page: Page | None = None
        self._storage: dict | None = None
        super().__init__(proxy, provider)

    def _get_proxy(self) -> dict | None:
        if not self._proxy:
            return None

        if isinstance(self._proxy, dict):
            return self._proxy

        parsed = urlparse(self._proxy)

        proxy = {"server": f"{parsed.scheme}://{parsed.hostname}:{parsed.port}"}

        if parsed.username:
            proxy["username"] = parsed.username

        if parsed.password:
            proxy["password"] = parsed.password

        return proxy

    def start(self) -> None:
        self._playwright = sync_playwright().start()

        if self._provider:
            cdp = self._provider.start()
            self._browser = self._playwright.chromium.connect_over_cdp(endpoint_url=cdp)
            self._context = self._browser.contexts[0]
            self._page = self._context.pages[0]
            logger.info("Playwright over CDP successfully started")

        else:
            self._browser = self._playwright.firefox.launch(headless=HEADLESS)
            self._context = self._browser.new_context()
            self._page = self._context.new_page()
            logger.info("Playwright successfully started")

    def close(self) -> None:
        if self._provider:
            self._provider.stop()

        if self._browser:
            self._browser.close()

        if self._playwright:
            self._playwright.stop()

        logger.info("Playwright successfully stopped")

    def get_page(self) -> Page:
        return self._page
