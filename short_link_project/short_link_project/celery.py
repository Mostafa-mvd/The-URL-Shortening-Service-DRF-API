import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'short_link_project.settings')

app = Celery('short_link_project')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    "delete-expired-short-links": {
        "task": "short_link_app.tasks.delete_expired_short_links",
        "schedule": crontab(minute="*/15")
    }
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
