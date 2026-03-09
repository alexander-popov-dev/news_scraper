from xml.etree import ElementTree

from src.core.abstract.parsers import BaseNewsParser
from src.core.dto import ArticleDTO
from src.sites.utils import parse_datetime_tz


class NewsParser(BaseNewsParser):

    def get_article_items(self, content: str) -> list:
        return ElementTree.fromstring(content).findall('channel/item')

    def parse_article_item(self, article, page_url: str, timezone: str | None) -> ArticleDTO:
        url = article.findtext('link')
        title = article.findtext('title')

        if not url or not title:
            raise ValueError(f'url={url!r}, title={title!r}')

        subtitle = article.findtext('description')
        published_at = article.findtext('pubDate', '')
        published_at = parse_datetime_tz(dt=published_at, tz=timezone)

        return ArticleDTO(url=url, title=title, subtitle=subtitle, published_at=published_at)
