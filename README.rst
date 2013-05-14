*********************
Django-Front
*********************

Django-front is a front-end editing application.

Installation
++++++++++++

* pip install django-front
* Add `front` to your INSTALLED_APPS
* `python manage.py migrate` (or syncdb if that's your dope)
* In your main template::

    `{% load front_tags %}`

    ...

    include jQuery, followed by front-editing scripts e.g.::

    `<script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>`
    `{% front_edit_scripts %}`

* In any template::

    `{% load front_tags %}`

    ...

    ```{% front_edit "placeholder_name" request.path request.LANGUAGE_CODE %}
        <p>Default when empty</p>
    {% end_front_edit  %}```

    Any variable passed after the name will be evaulauted. The full identifier (i.e. name and variables) will be hashed and will define the main identifier for this placeholder.

    So the content block in the above example will be rendered only at the page at this URL and the current language.

    This would be rendered on every page including this tag, in every language:


    ```{% front_edit "look ma, no hands" %}
        <p>Default when empty</p>
    {% end_front_edit  %}```


Requirements
++++++++++++

* Django 1.4+
* django-classy-tags

