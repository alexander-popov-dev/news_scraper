from parsel import Selector

from src.core.abstract.parsers import BaseNewsParser
from src.core.dto import ArticleDTO, ArticlesDTO
from src.sites.months_mapping import RUS_TO_ENG
from src.sites.utils import parse_datetime_months, parse_datetime_tz


class NewsParser(BaseNewsParser):
    ARTICLES_XPATH = '//div[@id="news-all"]//a'
    URL_XPATH = './@href'
    TITLE_XPATH = './/p[@class="title-z"]//text()'
    PUBLISHED_XPATH = './/p[@class="date-z"]/text()'

    def parse_news(self, content: str, page_url: str, timezone: str | None) -> ArticlesDTO:
        article_dto_list = []
        tree = Selector(text=content)

        if not tree:
            raise Exception('Failed to retrieve articles')

        for article in tree.xpath(self.ARTICLES_XPATH):
            url = article.xpath(self.URL_XPATH).get().strip()
            title = article.xpath(self.TITLE_XPATH).get().strip()
            published_at = article.xpath(self.PUBLISHED_XPATH).get().strip()
            published_at = parse_datetime_months(dt=published_at, months_map=RUS_TO_ENG)
            published_at = parse_datetime_tz(dt=published_at, tz=timezone)

            article_dto_list.append(
                ArticleDTO(
                    url=url,
                    title=title,
                    published_at=published_at
                )
            )

        return ArticlesDTO(articles=article_dto_list)
