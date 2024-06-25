from celery import Celery
from kombu import Exchange, Queue

from app import app

# BROKER_URL = 'amqp://guest:guest@localhost:5672//'
# app = Celery('tasks', broker='localhost')
# app = Celery('tasks', broker='amqp://guest:guest@127.0.0.1:5672//')
# app = Celery('tasks', broker='amqp://guest:guest@rabbitmq-service:5672//')

# app = Celery('tasks', broker='amqp://guest:guest@localhost :5672//')


# BROKER_URL = 'rabbitmqcli-124-rabbit@localhost'
# BROKER_URL = 'amqp://localhost//'
# BROKER_URL = 'amqp://guest:guest@[::1]:5672//'        # IPv6
# BROKER_URL = "amqp://host.docker.internal:5672"
# BROKER_URL = 'amqp://guest:guest@host.docker.internal:5672//'


# BROKER_URL = 'amqp://guest:guest@localhost:5672//'
BROKER_URL = "amqp://guest:guest@localhost:5673//"


def make_celery(app):
    celery = Celery(
        app.import_name,
        # broker=app.config['CELERY_BROKER_URL'],
        broker=BROKER_URL,
        # backend=app.config['CELERY_RESULT_BACKEND'],
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


celery = make_celery(app)
# celery.autodiscover_tasks(['app.main'])


default_exchange = Exchange("default", type="topic")
celery.conf.task_queues = (Queue("default", default_exchange, routing_key="default.#"),)

celery.conf.task_default_queue = "default"
celery.conf.task_default_exchange = "default"
celery.conf.task_default_routing_key = "default"

celery.autodiscover_tasks()

CELERY_TASK_ROUTES = {
    "default.*": {
        "queue": "default",
        "routing_key": "default.#",
    },
}

# from app.main.tasks import process_async_download
# celery.register_task(process_async_download)


# Community docker image:
# docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.13-management
