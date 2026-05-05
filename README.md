# News Scraper

A Django-based multi-site news scraper that collects articles from intellectual property and patent-related websites, stores them in PostgreSQL, and sends Telegram notifications on new findings.

## Features

- Scrapes 12 news sources (AGEPI, AIPO, COPAT, EPA, EPO, NIPO, Qazpatent, Sakpatenti, and more)
- Two scraping modes: HTTP requests (`RequestsClient`) and browser automation (`PlaywrightClient`)
- NST Browser integration for sites requiring browser fingerprinting
- Flexible pagination strategies: page-based, offset-based, single-page
- Celery task queue with three dedicated worker types
- Session tracking and raw response storage for debugging
- Telegram notifications when new articles are found
- Docker Compose deployment with Nginx reverse proxy

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Framework | Django 5.2 |
| Task Queue | Celery 5.6 + Redis |
| Browser Automation | Playwright 1.58 |
| HTTP Client | Requests 2.32 |
| HTML Parsing | Parsel (XPath/CSS) |
| Database | PostgreSQL |
| Server | Gunicorn + Nginx |
| Linting | Ruff |

## Project Structure

```
news_scraper/
├── server/             # Django project settings, Celery config, URL routing
├── src/
│   ├── core/
│   │   ├── abstract/   # Base classes for scrapers, parsers, repositories
│   │   ├── clients/    # RequestsClient, PlaywrightClient
│   │   ├── controllers/# NewsController — orchestrates the scraping workflow
│   │   ├── factories/  # NewsControllerFactory, ScrapingConfigsDTO
│   │   ├── pagination/ # PagePagination, OffsetPagination, SinglePageSource
│   │   ├── providers/  # NST Browser profile provider
│   │   ├── repositories/ # Django ORM persistence layer
│   │   ├── config_loader.py  # Dynamically loads per-site configs
│   │   ├── dto.py      # Request/Response/Article DTOs
│   │   └── enums.py    # Queues, session status, browser providers
│   ├── sites/          # Per-site scraper + parser + config (12 sites)
│   ├── models.py       # Session, Site, Article, BrowserProfile, RawResponseData
│   └── tasks.py        # Celery entry points
├── deploy/
│   ├── scraper/        # docker-compose.yaml, Dockerfile, Nginx config
│   └── database/       # PostgreSQL + Redis compose
├── .github/workflows/  # CI/CD: lint → build → deploy
├── Makefile
├── requirements.txt
└── .env.example
```

## Getting Started

### Prerequisites

- Python 3.13+
- PostgreSQL
- Redis
- Docker & Docker Compose (for production)

### Local Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium

# Copy and fill in environment variables
cp .env.example .env

# Apply migrations
python manage.py migrate

# Run development server
python manage.py runserver

# Start Celery worker (separate terminal)
celery -A server worker -l info
```

### Environment Variables

See `.env.example` for the full list. Key variables:

```env
SECRET_KEY=...
DEBUG=True

DB_NAME=news_scraper
DB_USER=postgres
DB_PASS=...
DB_HOST=localhost
DB_PORT=5432

CELERY_BROKER_URL=redis://localhost:6379/0

TELEGRAM_BOT=...
TELEGRAM_CHANNEL=...

# NST Browser (optional, for browser-based scrapers)
NST_BROWSER_API_KEY=...
NST_BROWSER_SERVER_IP=...
NST_BROWSER_SERVER_PORT=...
```

## Running Scrapers

Trigger scraping via a Celery task:

```python
from src.tasks import run_scraping_process_task

# Scrape all active sites
run_scraping_process_task.delay()

# Scrape specific sites by ID
run_scraping_process_task.delay(site_ids=[1, 3, 5])
```

Or schedule it via Celery Beat in the Django admin.

## Production Deployment

```bash
# Start all services
make up-prod

# View logs
make logs-prod

# Stop services
make down-prod
```

Docker Compose spins up six services:

| Service | Description | Concurrency |
|---------|-------------|-------------|
| `news-scraper-server` | Gunicorn + Django | — |
| `news-scraper-nginx` | Reverse proxy (port 80) | — |
| `news-scraper-beat` | Celery Beat scheduler | — |
| `news-scraper-manage-worker` | Task dispatch queue | 1 |
| `news-scraper-request-worker` | HTTP scraping queue | 10 |
| `news-scraper-browser-worker` | Browser scraping queue | 1 |

## Adding a New Site

1. Create `src/sites/{name}/` with `__init__.py`, `news/__init__.py`, `news/scraper.py`, `news/parser.py`
2. Implement `BaseScraper` and `BaseNewsParser`
3. Add `src/sites/{name}/config.py` with a `SCRAPING_CONFIGS` variable of type `ScrapingConfigsDTO`
4. Register the site in the database (`Site` model with the matching `package` name)

The `ConfigLoader` auto-discovers site configs by matching the `Site.package` field to the module path `src.sites.{package}.config`.

## Architecture

```
Celery task
    └── run_scraping_process_task
            └── creates Session
            └── for each Site → run_scraping_task
                    └── ConfigLoader loads site config
                    └── NewsControllerFactory builds NewsController
                    └── NewsController:
                            ├── Pagination generates URLs
                            ├── Scraper fetches raw HTML
                            ├── Raw response saved to DB
                            ├── Parser extracts articles (XPath/CSS)
                            └── Repository saves new articles
                    └── Telegram notification (if articles saved)
```

## Code Quality

```bash
# Lint
ruff check .

# Format
ruff format .
```

Pre-commit hooks are configured in `.pre-commit-config.yaml`.

## CI/CD

GitHub Actions runs on every push:
1. **Lint** — Ruff check + format validation
2. **Build** — Docker image build
3. **Deploy** — SSH deploy to production (main branch only)