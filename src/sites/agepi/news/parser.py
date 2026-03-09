from urllib.parse import unquote

from parsel import Selector

from src.core.abstract.parsers import BaseNewsParser
from src.core.dto import ArticleDTO
from src.sites.utils import parse_datetime_tz, get_base_url


class NewsParser(BaseNewsParser):
    ARTICLES_XPATH = '//div[@class="unformatted-list"]/div'
    URL_XPATH = './h4//a/@href'
    TITLE_XPATH = './h4//a/text()'
    PUBLISHED_XPATH = './div[@class="views-field views-field-field-press-release-type"]/div/text()'

    def get_article_items(self, content: str) -> list:
        return Selector(text=content).xpath(self.ARTICLES_XPATH)

    def parse_article_item(self, article, page_url: str, timezone: str | None) -> ArticleDTO:
        url = article.xpath(self.URL_XPATH).get()
        title = article.xpath(self.TITLE_XPATH).get()

        if not url or not title:
            raise ValueError(f'url={url!r}, title={title!r}')

        base_url = get_base_url(url=page_url)
        published_at_raw = article.xpath(self.PUBLISHED_XPATH).get('').strip()
        parts = published_at_raw.split()

        if not parts:
            raise ValueError(f'Could not parse published_at: {published_at_raw!r}')

        published_at = parse_datetime_tz(dt=parts[0], tz=timezone)

        return ArticleDTO(url=f'{base_url}{unquote(url.strip())}', title=title.strip(), published_at=published_at)
