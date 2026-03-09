from parsel import Selector

from src.core.abstract.parsers import BaseNewsParser
from src.core.dto import ArticleDTO
from src.sites.utils import parse_datetime_tz, get_base_url


class NewsParser(BaseNewsParser):
    ARTICLES_XPATH = '//ul[@class="list-unstyled py-2"]/li'
    URL_XPATH = './/a/@href'
    TITLE_XPATH = './/a/span/text()'
    SUBTITLE_XPATH = './/p[@class="card-text text-dark d-none d-md-block"]//text()'
    PUBLISHED_XPATH = './/p[@class="card-text text-dark vp-date mb-1"]//text()'

    def get_article_items(self, content: str) -> list:
        return Selector(text=content).xpath(self.ARTICLES_XPATH)

    def parse_article_item(self, article, page_url: str, timezone: str | None) -> ArticleDTO:
        url = article.xpath(self.URL_XPATH).get()
        title = article.xpath(self.TITLE_XPATH).get()

        if not url or not title:
            raise ValueError(f'url={url!r}, title={title!r}')

        base_url = get_base_url(url=page_url)
        subtitle = article.xpath(self.SUBTITLE_XPATH).get('').strip() or None
        published_at = article.xpath(self.PUBLISHED_XPATH).get('').strip()
        published_at = parse_datetime_tz(dt=published_at, tz=timezone, dayfirst=True)

        return ArticleDTO(url=f'{base_url}{url.strip()}', title=title.strip(), subtitle=subtitle, published_at=published_at)
