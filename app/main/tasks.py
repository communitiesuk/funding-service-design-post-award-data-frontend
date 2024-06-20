import time
from urllib.parse import urlencode

import redis  # type: ignore
import requests
from flask import current_app
from rq import Queue

redis_conn = redis.Redis(host="redis-data", port=6379, decode_responses=True)
q = Queue("find_data_download", connection=redis_conn)


def process_async_download(query_params: dict):
    request_url = (
        # Config.DATA_STORE_API_HOST
        "http://localhost:8080"
        + "/async_download"
        + ("?" + urlencode(query_params, doseq=True) if query_params else "")
    )
    requests.get(request_url)

    for i in range(10):
        print(f"Processing task {i}")
        time.sleep(1)

    return True


def add_download_task(query_params: dict):
    with current_app.app_context():
        job = q.enqueue(
            process_async_download,
            job_timeout=600,
            on_success=report_success,
            on_failure=report_failure,
            on_stopped=report_stopped,
            kwargs={"query_params": query_params},
            depends_on_kwargs={
                "query_params": query_params,
                "email": query_params["email_address"],
                "connection": redis_conn,
            },
        )

    q_len = len(q)
    current_app.logger.info(
        "Task (ID: {job_id}) added to queue , at {job_enqueued_at}. {q_len} tasks in queue. Requested by: {email}.",
        extra={
            "job_id": job.id,
            "job_enqueued_at": job.enqueued_at,
            "q_len": q_len,
            "email": query_params["email_address"],
        },
    )


def report_success(job, query_params=None, connection=None, result=None, *args, **kwargs):
    print("SUCCESS: job completed successfully.")


def report_failure(job, query_params=None, connection=None, type=None, value=None, traceback=None, *args, **kwargs):
    print("FAILURE: job failed.")


def report_stopped(job, query_params=None, connection=None, *args, **kwargs):
    print("STOPPED: job stopped.")
