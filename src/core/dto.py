import re
from datetime import datetime
from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class RequestDTO:
    """ Universal DTO encapsulating all HTTP request parameters for any fetcher implementation """
    url: str
    method: Optional[str] = None
    headers: Optional[Dict[str, str]] = None
    params: Optional[Dict[str, Any]] = None
    json: Optional[Dict[str, Any]] = None
    data: Optional[Any] = None
    cookies: Optional[Any] = None
    proxy: Optional[str] = None
    attempts: Optional[int] = None
    timeout: Optional[int] = None
    delay: Optional[int] = None
    allow_status_codes: Optional[list[int]] = None


@dataclass
class ResponseDTO:
    """ Universal DTO encapsulating HTTP response data including status and raw body """
    url: str
    status: int
    request_info: dict | None = None
    response: Optional[bytes] = None

    def text(self) -> str:
        """ Return body as text """
        headers = self.request_info.get('headers') if self.request_info else None

        if headers:
            content_type = headers.get('content-type', '')
            match = re.search(r'charset=([\w-]+)', content_type, re.IGNORECASE)

            if match:
                encoding = match.group(1)
                return self.response.decode(encoding, errors='strict')

        return self.response.decode('utf-8', errors='replace')

    def json(self) -> dict | None:
        """ Return body as JSON if possible """
        import json
        if isinstance(self.response, (str, bytes)):
            return json.loads(self.text())
        return None

    def bytes(self) -> bytes:
        """ Return body as bytes """
        if isinstance(self.response, str):
            return self.response.encode("utf-8")
        return self.response


@dataclass
class BrowserProviderDTO:
    id: int
    site_id: int
    provider: str
    is_active: bool
    profile_id: str
    folder_id: str | None = None


@dataclass
class ArticleDTO:
    url: str
    title: str
    subtitle: str | None = None
    content: str | None = None
    published_at: datetime | None = None


@dataclass
class ArticlesDTO:
    articles: list[ArticleDTO]
    site_id: int | None = None
    count: int | None = None

    def __post_init__(self):
        self.count = len(self.articles)


@dataclass
class SiteDTO:
    id: int
    url: str
    name: str
    package: str
    is_active: bool
    timezone: str | None = None
    proxy: str | None = None
    browser_provider: BrowserProviderDTO | None = None


@dataclass
class SitesDTO:
    sites: list[SiteDTO]
    count: int | None = None

    def __post_init__(self):
        self.count = len(self.sites)
