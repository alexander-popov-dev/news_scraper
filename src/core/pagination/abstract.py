from abc import abstractmethod, ABC
from typing import Iterator


class BasePagination(ABC):
    def __init__(self, url: str, start_page: int = 1):
        self.url = url
        self.page = start_page
        self._stop = False

    @abstractmethod
    def __iter__(self) -> Iterator[str]: ...

    def stop(self) -> None:
        self._stop = True
