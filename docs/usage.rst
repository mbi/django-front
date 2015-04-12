##################
Using django-front
##################

***************
Editing content
***************

1. As an authorized (and authenticated) user, hover your mouse pointer over a placeholder, it'll get a blue border.
2. Double-click to start editing.
3. After you're done editing:

   i) Click "save" to commit the changes to the database and get back to the default view, or
   ii) Click "cancel" to revert to the previously saved version, or
   iii) Click "history" to fetch the change history from the back-end. The button will turn into a select-box, displaying all the saved timestamps. Selecting a previous version will load the content from that version into the editor.


************************
Security considerations
************************

By default, only authenticated users having `the staff flag <https://docs.djangoproject.com/en/1.8/ref/contrib/auth/#django.contrib.auth.models.User.is_staff>`_ can edit placeholder content.

You can specify who can edit content in the settings: see ``DJANGO_FRONT_PERMISSION`` under :ref:`settings-section`.

Django-front will render its JavaScript object only to authenticated users with editing permissions.


************************
Performance
************************

* The first time a placeholder tag is rendered, its content fetched from the database and stored in Django's cache. Successive hits on that placeholder will get the content from the cache.
* Each time a placeholder is saved, its cache key is invalidated. A ``PlaceholderHistory`` object is also saved (if the content was changed).

.. warning:: To avoid hitting the database for each placeholder it is critical to use a proper cache back-end, such as `Memcached <https://docs.djangoproject.com/en/1.8/topics/cache/#memcached>`_.

************************
Caveats
************************

For users allowed to edit the content, ``django-front`` will wrap the rendered placeholder in a div, to mark it up as editable, e.g.::

    <body>
        <div class="editable" id="269cd2452ec9b17252d19eaa20719eedebec86a9">
            <h1>aaa</h1>
            <p>Lorem ipsum dolor sit amet, …</p>
        </div>
    </body>

(whitespace added for emphasis)

To non-authenticated users, the same placeholder will be rendered without the wrapping div::

    <body>
        <h1>aaa</h1>
        <p>Lorem ipsum dolor sit amet, …</p>
    </body>

As a consequence, CSS child selectors (e.g. ``body > h1``) will behave differently to authenticated users than non-authenticated ones. As a workaround, just keep in mind to extend the child selector to cover this case, e.g.::

    body > h1,
    body > .editable > h1 {
        …
    }



