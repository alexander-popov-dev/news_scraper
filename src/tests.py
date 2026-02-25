import logging

import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()
from src.tasks import run_scraping_process_task

# Create your tests here.
logging.basicConfig(level=logging.INFO)
if __name__ == '__main__':
    site_ids = {'site_ids': [10]}
    run_scraping_process_task.apply_async(kwargs=site_ids)
