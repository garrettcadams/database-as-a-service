import os

REDIS_PORT = os.getenv('DBAAS_NOTIFICATION_BROKER_PORT', '6379')
BROKER_URL = os.getenv('DBAAS_NOTIFICATION_BROKER_URL', 'redis://localhost:%s/0' % REDIS_PORT)
CELERYD_TASK_TIME_LIMIT=60
CELERY_TRACK_STARTED=True
CELERY_IGNORE_RESULT=False
CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend'