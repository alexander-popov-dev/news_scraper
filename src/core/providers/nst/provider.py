import logging

from server.settings import (
    NST_BROWSER_API_KEY,
    NST_BROWSER_SERVER_IP,
    NST_BROWSER_SERVER_PORT,
)
from src.core.clients.request.requests.client import RequestsClient
from src.core.decorators import retry
from src.core.dto import RequestDTO
from src.core.providers.abstract import BaseBrowserProvider

logger = logging.getLogger(__name__)


class NstBrowser(BaseBrowserProvider):
    def _get_headers(self) -> dict:
        """Create authorization headers for NST API requests"""
        return {"x-api-key": NST_BROWSER_API_KEY}

    @retry(retries=3, delay=10)
    def start(self) -> str:
        request_dto = RequestDTO(
            method="POST",
            url=f"http://{NST_BROWSER_SERVER_IP}:{NST_BROWSER_SERVER_PORT}/api/v2/browsers/{self._profile_id}",
            headers=self._get_headers(),
        )

        with RequestsClient() as client:
            response_dto = client.fetch(request_dto=request_dto)
            logger.info(f"NST Browser profile {self._profile_id} successfully started")

        port = response_dto.json()["data"]["port"]
        endpoint_cdp = f"http://localhost:{port}"

        return endpoint_cdp

    @retry(retries=3, delay=10)
    def stop(self) -> None:
        if self._close_profile:
            request_dto = RequestDTO(
                method="DELETE",
                url=f"http://{NST_BROWSER_SERVER_IP}:{NST_BROWSER_SERVER_PORT}/api/v2/browsers/{self._profile_id}",
                headers=self._get_headers(),
            )

            with RequestsClient() as client:
                client.fetch(request_dto=request_dto)
                logger.info(
                    f"NST Browser profile {self._profile_id} successfully stopped"
                )
