Installation
===============

Requirements
------------

Python requirements are automatically installed when you install via pip.

* Django-front supports Django 1.7 through 1.9
* django-classy-tags
* Python 2.6+ or Python 3.3+
* jQuery is required in your template


Installing django-front
-----------------------

* ``pip install django-front``
* Add ``front`` to your ``INSTALLED_APPS``
* Add a line to your ``urls.py``::

    urlpatterns += patterns('',
        url(r'^front-edit/', include('front.urls')),
    )

* ``python manage.py migrate`` (or syncdb if that's your dope)

* Note: the ``django.core.context_processors.request`` context processor must be enabled in your ``TEMPLATE_CONTEXT_PROCESSORS`` setting.


Testing
-------

* ``pip install tox && tox``
