from datetime import datetime
from zoneinfo import ZoneInfo

import dateutil
from dateutil.parser import parse
from urllib.parse import urlparse


def get_base_url(url: str) -> str:
    parsed_url = urlparse(url)
    return f'{parsed_url.scheme}://{parsed_url.netloc}'


def parse_datetime_tz(dt: str | datetime, tz: str, dayfirst: bool = False) -> datetime:
    if isinstance(dt, str):
        dt = parse(dt, dayfirst=dayfirst)

    if tz and dt.tzinfo is None:
        dt = dt.replace(tzinfo=ZoneInfo(tz))

    return dt.astimezone(ZoneInfo('UTC'))


def parse_datetime_months(dt: str, months_map: dict) -> str:
    dt = dt.lower()
    for other, eng_month in months_map.items():
        if other in dt:
            return dt.replace(other, eng_month)

    raise ValueError(f'Could not find {dt} in {months_map}')
