# from django.conf.urls import include, url
from django.conf.urls import url, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from test_project import views

urlpatterns = [
    url('', views.home, name='index'),
    url('ace', views.ace, name='ace'),
    url('epiceditor', views.epic, name='epic'),
    url('WYMeditor', views.WYMeditor, name='WYMeditor'),
    url(r'^front-edit/', include('front.urls')),
]

urlpatterns += staticfiles_urlpatterns()
