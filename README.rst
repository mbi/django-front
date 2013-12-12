Django-Front
*********************

Django-front is a front-end editing application: placeholders can be defined in Django templates, which can then be edited in the front-end (in place) by the site administrators.

.. image:: https://travis-ci.org/mbi/django-front.png?branch=master
  :target: http://travis-ci.org/mbi/django-front


Installation
++++++++++++

* ``pip install django-front``
* Add ``front`` to your ``INSTALLED_APPS``
* Add a line to your ``urls.py``::

    urlpatterns += patterns('',
        url(r'^front-edit/', include('front.urls')),
    )

* ``python manage.py migrate`` (or syncdb if that's your dope)

* Note: the ``django.core.context_processors.request`` context processor must be enabled in your ``TEMPLATE_CONTEXT_PROCESSORS`` setting.

Usage
+++++

In your main template
---------------------

At the top of your base template::

    {% load front_tags %}


Then include jQuery, followed by front-editing scripts e.g.::

    <script src="//ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js"></script>
    {% front_edit_scripts %}

The default editor just uses a plain ``<textarea>`` to edit the code.

* If you would like to use the `Ace <http://ace.ajax.org/>`_ editor::

    {% front_edit_scripts editor="ace" %}

Ace is loaded from a CDN, no extra installation is required.

Note: if the CDN solution doesn't work for you, install and serve Ace locally and use the `ace-local` plugin::

    <script src="{{STATIC_URL}}ace/src-min-noconflict/ace.js"></script>
    {% front_edit_scripts editor="ace-local" %}


* If you would like to use WYMeditor::

    {% front_edit_scripts editor="wymeditor" %}

To use WYMeditor, you'll have to install ``django-wymeditor``: ``pip install django-wymeditor``, then add ``wymeditor`` to your ``INSTALLED_APPS``.

* If you would like to use the `Redactor <http://imperavi.com/redactor/>`_ editor::

    {% front_edit_scripts editor="redactor" %}

Redactor being closed-source, it is not distributed with django-front: you'll have to `download <http://imperavi.com/redactor/download/>`_ and install it in your project:

* Copy ``redactor8xx`` into a directory being served as static file
* In the ``head`` of your master template, include the Redactor stylesheet::

    <link rel="stylesheet" type="text/css" href="{{STATIC_URL}}redactor8xx/redactor/redactor.css">

* In your master template, after the jQuery inclusion and before your ``{% front_edit_scripts editor="redactor" %}`` tag, include the Redactor JavaSript file::

    <script type="text/javascript" src="{{STATIC_URL}}redactor8xx/redactor/redactor.min.js"></script>

* If you would like to use `EpicEditor <http://epiceditor.com/>`_ editor for Markdown support::

    {% front_edit_scripts editor="epiceditor" %}

Defining placeholders in your templates
---------------------------------------

Once the ``front_edit_scripts`` scripts are injected (they are only rendered to users who can actually edit the content), you can start adding placeholders to your templates.

First load the tag library::

    {% load front_tags %}


Then define a placeholder::

    {% front_edit "placeholder_name" request.path request.LANGUAGE_CODE %}
        <p>Default when empty</p>
    {% end_front_edit  %}

Any variable passed after the name will be evaluated. The full identifier (i.e. name and variables) will be hashed and will define the main identifier for this placeholder.

The scope (visibility) of the rendered content block is defined by the variable names used in the block definition: the content block in the previous example will be rendered only on the page at the current URL, and the current language.

The following example, on the other hand, would be rendered on every page using the template having this tag, regardless of the language and the URL::


    {% front_edit "look ma, Im global!" %}
        <p>Default when empty</p>
    {% end_front_edit  %}


Settings
++++++++

These settings are defined, and can be overridden in your project settings

* ``DJANGO_FRONT_PERMISSION``: a callable that gets passed a user object, and returns a boolean specifying whether or not the user can do front-end editing. Defaults to ``lambda u: u and u.is_staff``
* ``DJANGO_FRONT_EDIT_MODE``: specifies whether the editor should be opened in a lightbox (default) or inline (over the edited element). Valid values are ``'inline'`` and ``'lightbox'``.
* ``DJANGO_FRONT_EDITOR_OPTIONS``: allows for options to be passed on to the editors (works with WYMeditor, Redactor, EpicEditor). This dictionary will be serialized as JSON and merged with the editor's base options. Defaults to ``{}``. Example, to handle `image uploads in Redactor <http://imperavi.com/redactor/docs/images/>`_::

    DJANGO_FRONT_EDITOR_OPTIONS = {
        'imageUpload': '/path/to/image/handling/view/'
    }


Performance
++++++++++++

The rendered content of each block is both persisted in the database and cached via Django's cache framework.

Requirements
++++++++++++

* Django 1.4+
* django-classy-tags
* Python 2.6+ or Python 3.3+

* jQuery is required in your template (see the "In your main template" above). If your website already uses jQuery you can use that instead. Please note that some versions of the WYMeditor don't work with recent versions of jQuery.
