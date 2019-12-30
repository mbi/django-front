# from django.conf.urls import include, url
from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include

from test_project import views

urlpatterns = [
    path('', views.home, name='index'),
    path('ace', views.ace, name='ace'),
    path('epiceditor', views.epic, name='epic'),
    path('WYMeditor', views.WYMeditor, name='WYMeditor'),
    url(r'^front-edit/', include('front.urls')),
]

urlpatterns += staticfiles_urlpatterns()
