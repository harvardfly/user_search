from celery import Celery

from user_search import settings_local

app = Celery(settings_local.settings['CELERY_SETTINGS']['namespace'])
app.config_from_object(
    'user_search:settings_local',
    namespace=settings_local.settings['CELERY_SETTINGS']['namespace']
)

app.conf.broker_url = settings_local.settings['CELERY_SETTINGS']['broker_url']
app.conf.result_backend = settings_local.settings['CELERY_SETTINGS']['result_backend']

app.autodiscover_tasks([
    'apps.rs_es'
])
