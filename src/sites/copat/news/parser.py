from parsel import Selector

from src.core.abstract.parsers import BaseNewsParser
from src.core.dto import ArticleDTO
from src.sites.utils import get_base_url, parse_datetime_tz


class NewsParser(BaseNewsParser):
    ARTICLES_XPATH = '//div[@class="single-post-wrapper"]/article'
    URL = './/a[@class="read-more btn submit"]/@href'
    TITLE = "./h3//text()"
    SUBTITLE = "./p//text()"
    PUBLISHED_XPATH = "./h6//text()"

    def get_article_items(self, content: str) -> list:
        return Selector(text=content).xpath(self.ARTICLES_XPATH)

    def parse_article_item(
        self, article, page_url: str, timezone: str | None
    ) -> ArticleDTO:
        url = article.xpath(self.URL).get()
        title = article.xpath(self.TITLE).get()

        if not url or not title:
            raise ValueError(f"url={url!r}, title={title!r}")

        base_url = get_base_url(url=page_url)
        subtitle = article.xpath(self.SUBTITLE).get("").strip() or None
        published_at = article.xpath(self.PUBLISHED_XPATH).get("").strip()
        published_at = parse_datetime_tz(dt=published_at, tz=timezone)

        return ArticleDTO(
            url=f"{base_url}{url.strip()}",
            title=title.strip(),
            subtitle=subtitle,
            published_at=published_at,
        )
