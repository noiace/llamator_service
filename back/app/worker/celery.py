from celery import Celery

from config import REDIS_URL

celery_app = Celery(
    'llm_worker',
    broker=REDIS_URL,
    include=["worker.tasks"]
)