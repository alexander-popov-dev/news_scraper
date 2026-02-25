from src.core.pagination.abstract import BasePagination


class PagePagination(BasePagination):

    def __iter__(self):
        page = self.page

        while not self._stop:
            yield self.url.format(page=page)
            page += 1


class OffsetPagination(BasePagination):
    def __init__(self, url: str, start_offset: int = 0, step: int = 9):
        super().__init__(url, start_offset)
        self.offset = start_offset
        self.step = step

    def __iter__(self):
        offset = self.offset

        while not self._stop:
            yield self.url.format(offset=offset)
            offset += self.step


class SinglePageSource(BasePagination):

    def __iter__(self):
        yield self.url
