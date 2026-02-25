from src.core.abstract.scrapers import BaseScraper
from src.core.dto import RequestDTO, ResponseDTO


class NewsScraper(BaseScraper):

    def run(self, url: str) -> ResponseDTO:
        request_dto = RequestDTO(method='GET', url=url)
        response_dto = self._client.fetch(request_dto=request_dto)

        return response_dto
