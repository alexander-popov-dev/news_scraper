from django.utils.dateparse import parse_datetime
from parsel import Selector

from src.core.abstract.parsers import BaseNewsParser
from src.core.dto import ArticleDTO, ArticlesDTO
from src.sites.months_mapping import UKR_TO_ENG
from src.sites.utils import parse_datetime_tz, parse_datetime_months


class NewsParser(BaseNewsParser):
    ARTICLES_XPATH = '//div[@class="elementor-widget-container"]//div[@class="blog-item"]'
    URL = './/a/@href'
    TITLE = './/a/text()'
    PUBLISHED_XPATH = './/div[@class="blog-meta"]/span[1]/text()'

    def parse_news(self, content: str, url: str, timezone: str | None) -> ArticlesDTO:
        article_dto_list = []
        tree = Selector(text=content)

        for article in tree.xpath(self.ARTICLES_XPATH):
            url = article.xpath(self.URL).get().strip()
            title = article.xpath(self.TITLE).get().strip()
            published_at = article.xpath(self.PUBLISHED_XPATH).get().strip()
            published_at = parse_datetime_months(dt=published_at, months_map=UKR_TO_ENG)
            published_at = parse_datetime_tz(dt=published_at, tz=timezone)

            article_dto_list.append(
                ArticleDTO(
                    url=url,
                    title=title,
                    published_at=published_at
                )
            )

        return ArticlesDTO(articles=article_dto_list)
