from celery import Celery

# celery_app = Celery(
#     __name__,
#     broker="redis://127.0.0.1:6379/0",
#     backend="redis://127.0.0.1:6379/0"
# )

celery_app = Celery(__name__, broker="redis://redis-data:6379/0", backend="redis://redis-data:6379/0")
