from django.contrib.staticfiles.storage import staticfiles_storage
from django.templatetags.static import static

from django.urls import reverse
from django.utils import timezone
from jinja2 import Environment


def environment(**options):
    env = Environment(**options)
    env.globals.update({
        # 'static': staticfiles_storage.url,
        'static': static,
        'url': reverse,
        'now': timezone.now
    })
    return env
