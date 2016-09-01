# from __future__ import absolute_import

import os

from celery import Celery
from redis import from_url

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NXT.settings')

# uncomment for development
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trololo.settings')

from django.conf import settings


class EnsomusCelery(Celery):
    def on_init(self, *args, **kwargs):
        r = from_url(settings.BROKER_URL)

        if r.exists(settings.SEND_MAIL_REDIS_LOCK_KEY):
            r.delete(settings.SEND_MAIL_REDIS_LOCK_KEY)


app = EnsomusCelery('ensomus_celery')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)