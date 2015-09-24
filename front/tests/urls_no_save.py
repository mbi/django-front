from django.conf.urls import url, include
from .views import test

urlpatterns = [
    url(r'^test/$', test, name='front-test'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
]
