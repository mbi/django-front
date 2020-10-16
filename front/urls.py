import django

from .views import do_save, get_history


if django.VERSION >= (3, 1, 0):
    from django.urls import re_path as url
else:
    from django.conf.urls import url


urlpatterns = [
    url(r'^save/$', do_save, name='front-placeholder-save'),
    url(
        r'^hist/(?P<key>[0-9a-f]{1,40})/$', get_history, name='front-placeholder-history'
    ),
]
