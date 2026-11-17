from abc import ABC, abstractmethod

from src.core.clients.abstract import BaseClient
from src.core.dto import ResponseDTO


class BaseScraper(ABC):
    def __init__(self, client: BaseClient) -> None:
        self._client = client

    @abstractmethod
    def run(self, url: str) -> ResponseDTO: ...
