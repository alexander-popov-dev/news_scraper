from enum import StrEnum


class CeleryQueue(StrEnum):
    MANAGE_QUEUE = "manage"
    BROWSER_SCRAPING_QUEUE = "browser_scraping"
    REQUEST_SCRAPING_QUEUE = "request_scraping"


class ScrapingDataType(StrEnum):
    NEWS = "NEWS"
    ARTICLES = "ARTICLES"


class SessionStatus(StrEnum):
    CREATED = "CREATED"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


class BrowserProvider(StrEnum):
    NSTBROWSER = "NSTBROWSER"
    MULTILOGIN = "MULTILOGIN"
