from urllib.parse import unquote
from parsel import Selector

from src.core.abstract.parsers import BaseNewsParser
from src.core.dto import ArticleDTO, ArticlesDTO
from src.sites.months_mapping import RUS_TO_ENG
from src.sites.utils import parse_datetime_mouths, parse_datetime_tz, get_base_url


class NewsParser(BaseNewsParser):
    ARTICLES_XPATH = '//div[@class="unformatted-list"]/div'
    URL_XPATH = './h4//a/@href'
    TITLE_XPATH = './h4//a/text()'
    PUBLISHED_XPATH = './div[@class="views-field views-field-field-press-release-type"]/div/text()'

    def parse_news(self, content: str, url: str, timezone: str | None) -> ArticlesDTO:
        article_dto_list = []
        tree = Selector(text=content)
        base_url = get_base_url(url=url)


        for article in tree.xpath(self.ARTICLES_XPATH):
            url = f'{base_url}{unquote(article.xpath(self.URL_XPATH).get().strip())}'
            title = article.xpath(self.TITLE_XPATH).get().strip()
            published_at = article.xpath(self.PUBLISHED_XPATH).get().strip()
            published_at = published_at.split()[0]
            published_at = parse_datetime_tz(dt=published_at, tz=timezone)

            article_dto_list.append(
                ArticleDTO(
                    url=url,
                    title=title,
                    published_at=published_at
                )
            )

        return ArticlesDTO(articles=article_dto_list)
