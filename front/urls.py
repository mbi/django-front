from django.conf.urls import url
from .views import do_save, get_history

urlpatterns = [
    url(r'^save/$', do_save, name='front-placeholder-save'),
    url(r'^hist/(?P<key>[0-9a-f]{1,40})/$', get_history, name='front-placeholder-history'),
]
