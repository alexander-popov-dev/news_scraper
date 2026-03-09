from abc import ABC, abstractmethod

from src.core.clients.abstract import BaseBrowserClient, BaseRequestClient
from src.core.dto import ResponseDTO


class BaseScraper(ABC):
    def __init__(self, client: BaseRequestClient | BaseBrowserClient) -> None:
        self._client = client

    @abstractmethod
    def run(self, url: str) -> ResponseDTO: ...
