from parsel import Selector

from src.core.abstract.parsers import BaseNewsParser
from src.core.dto import ArticleDTO
from src.sites.utils import parse_datetime_tz, get_base_url


class NewsParser(BaseNewsParser):
    ARTICLES_XPATH = '//div[contains(@id, "post")]'
    URL = './@id'
    TITLE = './/div[@class="news-short-content"]//text()'
    PUBLISHED_XPATH = 'normalize-space(.//div[@class="grid-date-post"])'

    def get_article_items(self, content: str) -> list:
        return Selector(text=content).xpath(self.ARTICLES_XPATH)

    def parse_article_item(self, article, page_url: str, timezone: str | None) -> ArticleDTO:
        url = article.xpath(self.URL).get()
        title = article.xpath(self.TITLE).get()

        if not url or not title:
            raise ValueError(f'url={url!r}, title={title!r}')

        base_url = get_base_url(url=page_url)
        published_at = article.xpath(self.PUBLISHED_XPATH).get('').strip()
        published_at = parse_datetime_tz(dt=published_at, tz=timezone)

        return ArticleDTO(url=f'{base_url}?{url.strip()}', title=title.strip(), published_at=published_at)
