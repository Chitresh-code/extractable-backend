import os
from celery import Celery

# Point Celery at Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "extractable.settings")

app = Celery("extractable")

# Pull config from Django settings with the CELERY_ prefix
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks.py in all installed apps
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
