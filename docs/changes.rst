Version history
###############

Version 0.5.3
=============
* Test against Django 1.10b1


Version 0.5.2
=============
* Fixes a possible unicode decode error on funky input


Version 0.5.1
=============
* Support for running tests via setuptools


Version 0.5.0
=============
* Supported Django versions are now 1.7, 1.8 and 1.9

Version 0.4.9
=============
* Wrap all JavaScript plugins in their distinct scope receiving a local jQuery

Version 0.4.8
=============
* Support for the Froala editor

Version 0.4.7
=============
* Upgraded the CDN and bundled versions of ACE, EPIC and CKEditor


Version 0.4.6
=============
* Test against Django 1.8

Version 0.4.5
=============
* Fixed editor history on RedactorJS > 10.0
* Fixed documentation
* Generate documentation during tox tests

Version 0.4.4
=============
* Added a missing migration
* Test against Django 1.8a
* Switched to tox

Version 0.4.3
=============
* Added an API allowing copying content from one Placeholder instance to another (e.g. same name, different arguments)

Version 0.4.2
=============
* Support for RedactorJS v10 API

Version 0.4.1
Version 0.4.0
=============
* Destroy editor before removing its container. Issues #6 and #7, thanks @syabro

Version 0.3.9
=============
* Test against Django 1.7 final
* Use event delegation instead of direct binding on .editable blocks

Version 0.3.8
=============
* Support both South and Django 1.7 native migrations, inspired by https://github.com/SmileyChris/easy-thumbnails

Version 0.3.7
=============
* Test against Django 1.7RC1

Version 0.3.6
=============
* Refactored JavaScript files to use "jQuery" instead of the shortcut ("$")

Version 0.3.5
=============
* Missing image in the EpicEditor static. (Issue #5, thanks @twined)

Version 0.3.3
=============
* Support for CKEditor

Version 0.3.2
=============
* Shipping with documentation

Version 0.3.0
=============
* History of content, possibility to move back to a previous version of the placeholder
* Massive rework of front-end side, modularization of editor plugins

Version 0.2.6
=============
* Added an "ace-local" plugin, for when Ace is served locally

Version 0.2.4
=============
* Add an extra class to the container, when the placeholder will be rendered empty
* Add a min-height on empty placeholders

Version 0.2.3
=============
* Make sure the urlconf entry was added properly
* Set a min-height on Redactor
* New DJANGO_FRONT_EDITOR_OPTIONS settings allows for options to be passed on to the editors (works with WYMeditor, Redactor, EpicEditor)

Version 0.2.2
=============
* Added support for the EpicEditor (thanks @daikeren - Issue #2)

Version 0.2.1
=============
* Clarified the installation section of the README (mentioned that django.core.context_processors.request needs to be enabled in TEMPLATE_CONTEXT_PROCESSORS)
* Added the test project to the settings, so that it's easier to run tests

Version 0.2.0
=============
* Test against Django 1.6b1

Version 0.1.9
=============
* Python 3.3 support on Django 1.5+

Version 0.1.8
=============
* Namespaced the layer and dialog CSS classes

Version 0.1.7
=============
* Editing mode (lightbox or inline)

Version 0.1.6
=============
* Support for Redactor 9 beta

Version 0.1.5
=============
* Support for the Redactor editor

Version 0.1.4
=============
* Include the Django Wymeditor theme, because django-wymeditor doesn't by default
* Push the STATIC_URL to the JavaScript context so that we don't have to assume it's /static/

Version 0.1.3
=============
* Basic test cases

Version 0.1.2
=============
* Support for WYMeditor (see note in README about installing django-wymeditor)

Version 0.1.1
=============
* Settings (permissions)
* Cleanups

Version 0.1.0
=============
* First release
