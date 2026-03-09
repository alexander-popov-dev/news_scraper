from src.core.abstract.scrapers import BaseScraper
from src.core.decorators import retry
from src.core.dto import RequestDTO, ResponseDTO


class NewsScraper(BaseScraper):
    @retry(retries=3, delay=10)
    def run(self, url: str) -> ResponseDTO:
        request_dto = RequestDTO(method="GET", url=url, timeout=30)
        response_dto = self._client.fetch(request_dto=request_dto)

        return response_dto
