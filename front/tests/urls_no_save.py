import django

from .views import test


if django.VERSION >= (3, 1, 0):
    from django.urls import re_path as url, include
else:
    from django.conf.urls import url, include

urlpatterns = [
    url(r'^test/$', test, name='front-test'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
]
