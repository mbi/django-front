Introduction
===============

Django-front is a front-end editing application: placeholders can be defined in Django templates, which can then be edited on the front-end (in place) by authorized users.

Features
--------

* Edit html content directly on the front-end of your site.
* Version history: jump back to a previous version of a content block at any time.
* Content blocks are persisted in the database, and in Django's cache (read: zero database queries)
* Content scope and inheritance: content blocks (placeholders) can be defined globally (i.e. edited once, displayed on every page), or on a single url, for a single language, …
* Built-in support for several content editor plugins (WYSIWYG, html, Markdown, …), adding a new editor is very simple.
