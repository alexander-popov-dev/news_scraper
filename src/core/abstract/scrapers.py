from abc import ABC, abstractmethod

from src.core.clients.abstract import BaseRequestClient, BaseBrowserClient
from src.core.dto import ResponseDTO


class BaseScraper(ABC):
    def __init__(self, client: BaseRequestClient | BaseBrowserClient) -> None:
        self._client = client

    @abstractmethod
    def run(self, url: str) -> ResponseDTO: ...


# class BaseRequestScraper(BaseScraper):
#
#     def __init__(self, client: BaseRequestClient) -> None:
#         self._client = client
#
#     @abstractmethod
#     def run(self, url: str) -> ResponseDTO: ...
#
#
# class BaseBrowserScraper(BaseScraper):
#
#     def __init__(self, client: BaseBrowserClient) -> None:
#         self._client = client
#
#     @abstractmethod
#     def run(self, url: str) -> ResponseDTO: ...
