Installation
===============

Requirements
------------

* Django-front supports Django 4.2 and 5.0
* django-classy-tags
* Python 3.9+
* jQuery is required in your template


Installing django-front
-----------------------

* ``pip install django-front``
* Add ``front`` to your ``INSTALLED_APPS``
* Add a line to your ``urls.py``::

    urlpatterns += [
        url(r'^front-edit/', include('front.urls')),
    ]

* ``python manage.py migrate`` (or syncdb if that's your dope)

* Note: the ``django.core.context_processors.request`` context processor must be enabled in your ``TEMPLATE_CONTEXT_PROCESSORS`` setting.


Testing
-------

* ``pip install --upgrade tox && tox``
