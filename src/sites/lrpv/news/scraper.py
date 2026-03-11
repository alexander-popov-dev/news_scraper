from src.core.abstract.scrapers import BaseScraper
from src.core.decorators import retry
from src.core.dto import RequestDTO, ResponseDTO


class NewsScraper(BaseScraper):
    @retry(retries=3, delay=10)
    def run(self, url: str) -> ResponseDTO:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/144.0.0.0 Safari/537.36"
            )
        }
        request_dto = RequestDTO(method="GET", url=url, headers=headers, timeout=30)
        response_dto = self._client.fetch(request_dto=request_dto)

        return response_dto
