import logging
import time
from functools import wraps
from typing import Callable, Any

logger = logging.getLogger(__name__)


def retry(retries: int = 3, delay: float = 1.0):
    """
    Decorator for retrying a synchronous function on exception.
    Retries the function up to `retries` times with `delay` seconds between attempts.
    Raises the last exception if all retries fail.
    """

    def decorator(func: Callable[..., Any]):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None

            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    logger.error(f'Attempt {attempt} failed for {func.__name__}: {e}')

                    if attempt < retries:
                        time.sleep(delay)

            raise last_error

        return wrapper

    return decorator
