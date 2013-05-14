Django-Front
*********************

Django-front is a front-end editing application.

Installation
++++++++++++

* ``pip install django-front``
* Add ``front`` to your ``INSTALLED_APPS``
* Add a line to urlconf::

    urlpatterns += patterns('',
        url(r'^front-edit/', include('front.urls')),
    )

* ``python manage.py migrate`` (or syncdb if that's your dope)

Usage
+++++


In your main template::

    {% load front_tags %}


Then include jQuery, followed by front-editing scripts e.g.::

    <script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
    {% front_edit_scripts %}

or, if you would like to use the `ACE <http://ace.ajax.org/>`_ editor::

    {% front_edit_scripts editor="ace" %}



In any template::

    {% load front_tags %}

    ...

    {% front_edit "placeholder_name" request.path request.LANGUAGE_CODE %}
        <p>Default when empty</p>
    {% end_front_edit  %}

Any variable passed after the name will be evaluauted. The full identifier (i.e. name and variables) will be hashed and will define the main identifier for this placeholder.

So the content block in the above example will be rendered only at the page at this URL and the current language.

This would be rendered on every page including this tag, in every language::


    {% front_edit "look ma, no hands" %}
        <p>Default when empty</p>
    {% end_front_edit  %}


Settings
++++++++

You can define these in your settings:

* ``DJANGO_FRONT_PERMISSION``: a callable that gets passed a user object, and returns a Boolean specifying whether or not the user can do front-end editing. Defaults to ``lambda u: u and u.is_staff``


Performance
++++++++++++

The content of each block is both persisted in the database and cached via Django's cache framework (the obviously hit first)

Requirements
++++++++++++

* Django 1.4+
* django-classy-tags

