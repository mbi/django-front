from django.conf.urls import patterns, url

urlpatterns = patterns(
    'front.views',
    url(r'^save/$', 'do_save', name='front-placeholder-save'),
    url(r'^hist/(?P<key>[0-9a-f]{1,40})/$', 'get_history', name='front-placeholder-history'),
)
