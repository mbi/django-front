try:
    from django.conf.urls import url, patterns, include
except ImportError:
    from django.conf.urls.defaults import url, patterns, include

urlpatterns = patterns('',
    url(r'^test/$', 'front.tests.views.test', name='front-test'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    # url(r'^front-edit/', include('front.urls'))
)
