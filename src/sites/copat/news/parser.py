from parsel import Selector

from src.core.dto import ArticlesDTO, ArticleDTO

from src.core.abstract.parsers import BaseNewsParser
from src.sites.utils import parse_datetime_tz, get_base_url


class NewsParser(BaseNewsParser):
    ARTICLES_XPATH = '//div[@class="single-post-wrapper"]/article'
    URL = './/a[@class="read-more btn submit"]/@href'
    TITLE = './h3//text()'
    SUBTITLE = './p//text()'
    PUBLISHED_XPATH = './h6//text()'

    def parse_news(self, content: str, page_url: str, timezone: str | None) -> ArticlesDTO:
        article_dto_list = []
        tree = Selector(text=content)
        base_url = get_base_url(url=page_url)

        if not tree:
            raise Exception('Failed to retrieve articles')

        for article in tree.xpath(self.ARTICLES_XPATH):
            url = f'{base_url}{article.xpath(self.URL).get().strip()}'
            title = article.xpath(self.TITLE).get().strip()
            subtitle = article.xpath(self.SUBTITLE).get().strip()
            published_at = article.xpath(self.PUBLISHED_XPATH).get().strip()
            published_at = parse_datetime_tz(dt=published_at, tz=timezone)

            article_dto_list.append(
                ArticleDTO(
                    url=url,
                    title=title,
                    subtitle=subtitle,
                    published_at=published_at
                )
            )

        return ArticlesDTO(articles=article_dto_list)
