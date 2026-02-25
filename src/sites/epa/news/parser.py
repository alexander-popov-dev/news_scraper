from parsel import Selector

from src.core.dto import ArticlesDTO, ArticleDTO

from src.core.abstract.parsers import BaseNewsParser

from src.sites.utils import parse_datetime_tz, get_base_url


class NewsParser(BaseNewsParser):
    ARTICLES_XPATH = '//ul[@class="list-unstyled py-2"]/li'
    URL_XPATH = './/a/@href'
    TITLE_XPATH = './/a/span/text()'
    SUBTITLE_XPATH = './/p[@class="card-text text-dark d-none d-md-block"]//text()'
    PUBLISHED_XPATH = './/p[@class="card-text text-dark vp-date mb-1"]//text()'

    def parse_news(self, content: str, url: str, timezone: str | None) -> ArticlesDTO:
        article_dto_list = []
        tree = Selector(text=content)
        base_url = get_base_url(url=url)

        for article in tree.xpath(self.ARTICLES_XPATH):
            url = f'{base_url}{article.xpath(self.URL_XPATH).get().strip()}'
            title = article.xpath(self.TITLE_XPATH).get().strip()
            subtitle = article.xpath(self.SUBTITLE_XPATH).get().strip()
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

        return ArticlesDTO(articles=article_dto_list)
