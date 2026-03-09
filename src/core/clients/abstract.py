from abc import ABC, abstractmethod
from typing import Self

from playwright.sync_api import Page

from src.core.dto import RequestDTO, ResponseDTO
from src.core.providers.abstract import BaseBrowserProvider


class BaseClient(ABC):
    def __init__(
        self,
        proxy: str | dict | None = None,
        provider: BaseBrowserProvider | None = None,
    ) -> None:
        self._proxy = proxy
        self._provider = provider

    @abstractmethod
    def start(self) -> None: ...

    @abstractmethod
    def close(self) -> None: ...

    def __enter__(self) -> Self:
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()


class BaseRequestClient(BaseClient):
    @abstractmethod
    def start(self) -> None: ...

    @abstractmethod
    def close(self) -> None: ...

    @abstractmethod
    def fetch(self, request_dto: RequestDTO) -> ResponseDTO: ...


class BaseBrowserClient(BaseClient):
    @abstractmethod
    def start(self) -> None: ...

    @abstractmethod
    def close(self) -> None: ...

    @abstractmethod
    def get_page(self) -> Page: ...
