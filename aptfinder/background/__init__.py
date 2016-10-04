from celery import Celery

from .. import celery_config

celery = Celery(__name__, config_source=celery_config)
