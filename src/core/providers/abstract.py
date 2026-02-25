from abc import ABC, abstractmethod


class BaseBrowserProvider(ABC):

    def __init__(self, profile_id: str, folder_id: str | None = None, close_profile: bool = True) -> None:
        self._profile_id = profile_id
        self._folder_id = folder_id
        self._close_profile = close_profile

    @abstractmethod
    def start(self) -> str:
        ...

    @abstractmethod
    def stop(self) -> None:
        ...
