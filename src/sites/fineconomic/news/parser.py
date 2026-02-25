from parsel import Selector

from src.core.dto import ArticlesDTO, ArticleDTO

from src.core.abstract.parsers import BaseNewsParser
from src.sites.utils import parse_datetime_tz, get_base_url


class NewsParser(BaseNewsParser):
    ARTICLES_XPATH = '//div[@class="form-news__column"]'
    URL = './a/@href'
    TITLE = './/div[@class="form-news__title"]//text()'
    SUBTITLE = './/div[@class="form-news__text"]//p[{i}]//text()'
    PUBLISHED_XPATH = './/div[@class="form-news__date"]//text()'

    def parse_news(self, content: str, url: str, timezone: str | None) -> ArticlesDTO:
        article_dto_list = []
        tree = Selector(text=content)
        base_url = get_base_url(url=url)
        element_index = 1

        for article in tree.xpath(self.ARTICLES_XPATH):
            url = f'{base_url}{article.xpath(self.URL).get().strip()}'
            title = article.xpath(self.TITLE).get().strip()
            subtitle = article.xpath(self.SUBTITLE.format(i=element_index)).get().strip()
            published_at = article.xpath(self.PUBLISHED_XPATH).get().strip()
            published_at = parse_datetime_tz(dt=published_at, tz=timezone, dayfirst=True)

            article_dto_list.append(
                ArticleDTO(
                    url=url,
                    title=title,
                    subtitle=subtitle,
                    published_at=published_at
                )
            )

            element_index += 1

        return ArticlesDTO(articles=article_dto_list)
