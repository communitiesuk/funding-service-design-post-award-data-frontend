from time import sleep
from urllib.parse import urlencode

import requests
from celery import shared_task

from config import Config


@shared_task(ignore_result=False)
def process_async_download(query_params: dict):
    for i in range(10):
        print(f"Processing async download {i}")
        sleep(1)

    request_url = (
        Config.DATA_STORE_API_HOST
        + "/async_download"
        + ("?" + urlencode(query_params, doseq=True) if query_params else "")
    )
    requests.get(request_url)
