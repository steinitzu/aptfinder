import os

BROKER_URL = os.environ['AMQP_URL']
CELERY_RESULT_BACKEND = os.environ['REDIS_URL']
