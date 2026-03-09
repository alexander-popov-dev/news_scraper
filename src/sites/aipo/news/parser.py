from parsel import Selector

from src.core.abstract.parsers import BaseNewsParser
from src.core.dto import ArticleDTO
from src.sites.months_mapping import RUS_TO_ENG
from src.sites.utils import parse_datetime_months, parse_datetime_tz


class NewsParser(BaseNewsParser):
    ARTICLES_XPATH = '//div[@class="blog-one-text"]'
    URL = ".//a/@href"
    TITLE = ".//h3/a/text()"
    SUBTITLE = "./p//text()"
    PUBLISHED_XPATH = ".//li[2]/text()"

    def get_article_items(self, content: str) -> list:
        return Selector(text=content).xpath(self.ARTICLES_XPATH)

    def parse_article_item(
        self, article, page_url: str, timezone: str | None
    ) -> ArticleDTO:
        url = article.xpath(self.URL).get()
        title = article.xpath(self.TITLE).get()

        if not url or not title:
            raise ValueError(f"url={url!r}, title={title!r}")

        subtitle = article.xpath(self.SUBTITLE).get("").strip() or None
        published_at = article.xpath(self.PUBLISHED_XPATH).get("").strip()
        published_at = parse_datetime_months(dt=published_at, months_map=RUS_TO_ENG)
        published_at = parse_datetime_tz(dt=published_at, tz=timezone)

        return ArticleDTO(
            url=url.strip(),
            title=title.strip(),
            subtitle=subtitle,
            published_at=published_at,
        )
