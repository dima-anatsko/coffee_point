from django.templatetags.static import static

from django.urls import reverse
from django.utils import timezone
from jinja2 import Environment


def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': static,
        'url': reverse,
        'now': timezone.now
    })
    return env
