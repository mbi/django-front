try:
    from django.conf.urls import *
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import *


urlpatterns = patterns('front.views',
    url(r'^save/$', 'do_save', name='front-placeholder-save'),
)
