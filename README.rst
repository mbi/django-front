Django-Front
*********************

Django-front is a front-end editing application: placeholders can be defined in Django templates, which can then be edited in the front-end (in place) by the site administrators.

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


In your main template
---------------------

At the top of your base template::

    {% load front_tags %}
    
Then include jQuery, followed by front-editing scripts e.g.::

    <script src="//ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js"></script>
    {% front_edit_scripts %}

or, if you would like to use the `ACE <http://ace.ajax.org/>`_ editor::

    {% front_edit_scripts editor="ace" %}

or, if you would like to use WYMeditor::

    {% front_edit_scripts editor="wymeditor" %}

To use WYMeditor, you'll have to install ``django-wymeditor``: ``pip install django-wymeditor``, then add ``wymeditor`` to your ``INSTALLED_APPS``.


In any template
---------------

In any (other) template, where you want to define your placeholder blocks::

    {% load front_tags %}

    ...

    {% front_edit "placeholder_name" request.path request.LANGUAGE_CODE %}
        <p>Default when empty</p>
    {% end_front_edit  %}

Any variable passed after the name will be evaluauted. The full identifier (i.e. name and variables) will be hashed and will define the main identifier for this placeholder.

The content block in the previous example will be rendered only on the page at the current URL, and the current language.

The following example, on the other hand, would be rendered on every page using the template having this tag, regardless of the language and the URL::


    {% front_edit "look ma, Im global!" %}
        <p>Default when empty</p>
    {% end_front_edit  %}


Settings
++++++++

You can define these in your settings:

* ``DJANGO_FRONT_PERMISSION``: a callable that gets passed a user object, and returns a Boolean specifying whether or not the user can do front-end editing. Defaults to ``lambda u: u and u.is_staff``


Performance
++++++++++++

The content of each block is both persisted in the database and cached via Django's cache framework

Requirements
++++++++++++

* Django 1.4+
* django-classy-tags

