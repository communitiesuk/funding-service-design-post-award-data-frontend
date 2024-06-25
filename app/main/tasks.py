# from app import celery
from time import sleep
from urllib.parse import urlencode

import requests

from config import Config
from config.celery_config import celery


@celery.task(name="default.app.main.tasks.process_async_download")
def process_async_download(query_params: dict):
    for i in range(5):
        print(f"Processing...{i}")
        sleep(1)

    request_url = (
        Config.DATA_STORE_API_HOST
        + "/async_download"
        + ("?" + urlencode(query_params, doseq=True) if query_params else "")
    )
    requests.get(request_url)
