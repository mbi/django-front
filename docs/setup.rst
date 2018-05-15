##############
Setting it up
##############


***************
Template layout
***************

We assume that your site uses a `basic template hierarchy <https://docs.djangoproject.com/en/1.8/topics/templates/#template-inheritance>`_, having a base template and multiple "content" templates inheriting from the base one.

To set up `django-front`, you will need to include a few lines in your base template, then add content placeholders in the child templates.

*******************
Your base template…
*******************

First, load the `front_tags` module at the top of your base template::

    {% load front_tags %}


Then include jQuery, followed by front-editing scripts somewhere towards the end of your ``<body>``, e.g.::

    <script src="//ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js"></script>
    {% front_edit_scripts %}

.. note::

    the Redactor editor needs a fairly recent version of jQuery (1.8+), but WYMeditor will need an older one (<= 1.7). Adapt as needed.

**********************************************
Defining placeholders in your child templates…
**********************************************

Once the ``front_edit_scripts`` scripts are injected (they are only rendered to users who can actually edit the content), you can start adding placeholders to your templates.

First load the tag library::

    {% load front_tags %}

Then define a placeholder::

    {% front_edit "placeholder_name" request.path request.LANGUAGE_CODE %}
        <p>Default when empty</p>
    {% end_front_edit  %}

When no placeholder content is defined for this placeholder, the default content is displayed instead.

Placeholder scope
=================

Any variable passed after the placeholder name will be evaluated. The full identifier (i.e. name and variables) will be hashed and will define the main identifier for this placeholder.

The scope (visibility) of the rendered content block is defined by the variable names used in the block definition: the content block in the previous example will be rendered only on the page at the current URL, and the current language.

The following example, on the other hand, would be rendered on every page using the template having this tag, regardless of the language and the URL::

    {% front_edit "look ma, Im global!" %}
        <p>Default when empty</p>
    {% end_front_edit  %}

******************
Choosing an editor
******************

The default editor just uses a plain ``<textarea>`` to edit the html code, not too fancy.

You can pass an argument to the ``front_edit_scripts`` tag added in the base template, to specify the editor to use.


Ace editor
===========

`Ace <http://ace.ajax.org/>`_ is an embeddable code editor written in JavaScript, it is used by GitHub and the Khan Academy, among others.

To use the Ace editor::

    {% front_edit_scripts editor="ace" %}

Ace is loaded from a CDN, no extra installation is required.

NOTE: if the CDN solution doesn't work for you, `download Ace <https://github.com/ajaxorg/ace-builds/>`_ and serve it locally and use the `ace-local` plugin::

    <script src="{{STATIC_URL}}ace/src-min-noconflict/ace.js"></script>
    {% front_edit_scripts editor="ace-local" %}


WYMeditor
===========

`WYMeditor <http://www.wymeditor.org/>`_ is a web-based WYSIWYM (What You See Is What You Mean) XHTML editor

You'll have to install ``django-wymeditor``: ``pip install django-wymeditor``, then add ``wymeditor`` to your ``INSTALLED_APPS``, then::

    {% front_edit_scripts editor="wymeditor" %}

Redactor
========

`Redactor <http://imperavi.com/redactor/>`_ is a commercial WYSIWYG html editor.

To use the Redactor editor::

    {% front_edit_scripts editor="redactor" %}

Redactor being closed-source, it is not distributed with django-front: you'll have to `download it <http://imperavi.com/redactor/download/>`_ and install it in your project:

1. Copy ``redactor9xx`` into a directory being served as static file
2. In the ``head`` of your master template, include the Redactor stylesheet::

    <link rel="stylesheet" type="text/css" href="{{STATIC_URL}}redactor9xx/redactor/redactor.css">

3. In your master template, after the jQuery inclusion and before your ``{% front_edit_scripts editor="redactor" %}`` tag, include the Redactor JavaSript file::

    <script type="text/javascript" src="{{STATIC_URL}}redactor9xx/redactor/redactor.min.js"></script>

(Replace ``redactor9xx`` with the build number you've downloaded)


CKEditor
========
`CKEditor <http://ckeditor.com/>`_ is a ready-for-use HTML text editor designed to simplify web content creation.

To use CKEditor editor, make sure that the ``ckeditor.js`` script is loaded in your base template, (or load it from a CDN: ``<script src="//cdn.ckeditor.com/4.4.7/standard/ckeditor.js"></script>``), then::

    {% front_edit_scripts editor="ckeditor" %}


EpicEditor
===========

`EpicEditor <http://epiceditor.com/>`_ is an embeddable JavaScript Markdown editor.

To use EpicEditor::

    {% front_edit_scripts editor="epiceditor" %}

The EpicEditor scripts are served directly from django-front's static folders, no need to include anything else in your base template.


Froala
======

`Froala <https://editor.froala.com/>`_ is a commercial WYSIWYG html editor. It is free to use for personal and non-profit projects.

Froala being closed-source, it is not distributed with django-front: you'll have to `download <https://editor.froala.com/pricing>`_ and install it in your project.
Alternatively it can be served from a CDN.

In your ``<head>``::

    <link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/font-awesome/4.2.0/css/font-awesome.min.css">
    <link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/froala-editor/1.2.6/css/froala_editor.min.css">
    <link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/froala-editor/1.2.6/css/themes/gray.min.css">

At the end of your ``<body>``::

    <script src="//cdnjs.cloudflare.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>
    <script src="//cdnjs.cloudflare.com/ajax/libs/froala-editor/1.2.6/js/froala_editor.min.js"></script>
    {% front_edit_scripts editor="froala" %}


Froala accepts `options <https://editor.froala.com/options>`_ that can be passed to the editor via the ``DJANGO_FRONT_EDITOR_OPTIONS`` settings (see the next section).


Medium Editor
=============

`Medium Editor <https://yabwe.github.io/medium-editor/>`_ is a Medium.com WYSIWYG editor clone. Uses contenteditable API to implement a rich text solution.

In your ``<head>``::

    <link rel="stylesheet" href="//cdn.jsdelivr.net/medium-editor/latest/css/medium-editor.min.css">
    <link rel="stylesheet" href="//cdn.jsdelivr.net/medium-editor/latest/css/themes/beagle.min.css">


At the end of your ``<body>``::

    <script src="//cdnjs.cloudflare.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>
    <script src="//cdn.jsdelivr.net/medium-editor/latest/js/medium-editor.min.js"></script>
    {% front_edit_scripts editor="medium" %}

The Medium Editor accepts `setting options <https://github.com/yabwe/medium-editor#mediumeditor-options>`_ that can be passed to the editor via the ``DJANGO_FRONT_EDITOR_OPTIONS`` settings (see the next section).

Summernote
==========

`Summernote <https://summernote.org/>`_ is an open-source WYSIWYG Editor based on Bootstrap.

In your ``<head>``::

    <link href="https://cdnjs.cloudflare.com/ajax/libs/summernote/0.8.9/summernote-lite.css" rel="stylesheet">


At the end of your ``<body>``::

    <script src="//cdnjs.cloudflare.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/summernote/0.8.9/summernote-lite.js"></script>
    {% front_edit_scripts editor="summernote" %}

The `Summernote editor accepts options <https://summernote.org/deep-dive/>`_ that can be passed to the editor via the ``DJANGO_FRONT_EDITOR_OPTIONS`` settings (see the next section).


*******************************
Passing arguments to the editor
*******************************

You can pass extra initialization arguments to some of the editors, to e.g. handle file uploads or load plugins. See: ``DJANGO_FRONT_EDITOR_OPTIONS`` under :ref:`settings-section`

********************
Add your own editor
********************

To add support for a new editor type (say "foo"):

1. Add ``['foo', ]`` to ``DJANGO_FRONT_ALLOWED_EDITORS`` in your settings. See: :ref:`settings-section`
2. Add a ``/static/front/js/front-edit.foo.js`` file, you'll need to provide the following function prototype (here as an example for the default editor, see more examples in `static/front/js <https://github.com/mbi/django-front/tree/master/front/static/front/js>`_) ::

    (function(jQuery){
        window.front_edit_plugin = {

            target: null,

            // Returns the html that will contain the editor
            get_container_html: function(element_id, front_edit_options) {
                return '<textarea class="front-edit-container" id="edit-'+ element_id +'"></textarea>';
            },

            // initializes the editor on the target element, with the given html code
            set_html: function(target, html, front_edit_options) {
                this.target = target;
                this.target.find('.front-edit-container').html(html);
            },

            // returns the edited html code
            get_html: function(front_edit_options) {
                return this.target.find('.front-edit-container').val();
            },

            // destroy the editor
            destroy_editor: function() {
                self.target = null;
            }
        };
    })(jQuery);


3. Maybe submit a pull request?
