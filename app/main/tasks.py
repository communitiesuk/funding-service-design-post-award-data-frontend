import time
from urllib.parse import urlencode

import redis  # type: ignore
import requests
from rq import Queue

from config import Config

r = redis.Redis()
q = Queue(connection=r)


def process_async_download(query_params: dict):
    request_url = (
        Config.DATA_STORE_API_HOST
        + "/async_download"
        + ("?" + urlencode(query_params, doseq=True) if query_params else "")
    )
    requests.get(request_url)


def add_download_task(query_params: dict):
    job = q.enqueue(process_async_download, query_params)
    q_len = len(q)
    time.sleep(2)
    return f"Added task to queue: {job.id}, at {job.enqueued_at}. {q_len} tasks in queue."
