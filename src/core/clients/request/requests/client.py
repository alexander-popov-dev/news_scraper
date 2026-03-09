import logging
from typing import Optional

import requests
from requests import Session

from src.core.clients.abstract import BaseRequestClient
from src.core.dto import RequestDTO, ResponseDTO
from src.core.providers.abstract import BaseBrowserProvider

logger = logging.getLogger(__name__)


class RequestsClient(BaseRequestClient):
    def __init__(
        self,
        proxy: str | dict | None = None,
        provider: BaseBrowserProvider | None = None,
    ) -> None:
        self._session: Optional[Session] = None
        super().__init__(proxy, provider)

    def start(self):
        self._session = requests.Session()
        logger.info("Requests session successfully started")

    def close(self):
        if self._session:
            self._session.close()
        logger.info("Requests session successfully stopped")

    def fetch(self, request_dto: RequestDTO) -> ResponseDTO:
        response = self._session.request(
            method=request_dto.method,
            url=request_dto.url,
            headers=request_dto.headers,
            params=request_dto.params,
            json=request_dto.json,
            data=request_dto.data,
            cookies=request_dto.cookies,
            proxies={"http": self._proxy, "https": self._proxy}
            if self._proxy
            else None,
            timeout=request_dto.timeout,
        )

        response.raise_for_status()

        return ResponseDTO(
            url=response.url,
            status=response.status_code,
            request_info={
                "method": response.request.method,
                "headers": dict(response.request.headers),
                "body": response.request.body,
            },
            response=response.content,
        )
