from xml.etree import ElementTree
from src.core.abstract.parsers import BaseNewsParser
from src.core.dto import ArticleDTO, ArticlesDTO
from src.sites.utils import parse_datetime_tz


class NewsParser(BaseNewsParser):

    def parse_news(self, content: str, page_url: str, timezone: str | None) -> ArticlesDTO:
        article_dto_list = []
        tree = ElementTree.fromstring(content)

        if not tree:
            raise Exception('Failed to retrieve articles')

        for article in tree.findall('channel/item'):
            url = article.find('link').text
            title = article.find('title').text
            subtitle = article.find('description').text
            published_at = article.find('pubDate').text
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
