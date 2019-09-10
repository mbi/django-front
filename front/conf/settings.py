from django.conf import settings

DJANGO_FRONT_PERMISSION = getattr(settings, 'DJANGO_FRONT_PERMISSION', lambda u: u and u.is_staff)
DJANGO_FRONT_EDIT_MODE = getattr(settings, 'DJANGO_FRONT_EDIT_MODE', 'lightbox')  # ('lightbox' or 'inline')
DJANGO_FRONT_EDITOR_OPTIONS = getattr(settings, 'DJANGO_FRONT_EDITOR_OPTIONS', dict())
DJANGO_FRONT_ALLOWED_EDITORS = [editor.lower() for editor in getattr(settings, 'DJANGO_FRONT_ALLOWED_EDITORS', ['ace', 'ace-local', 'wymeditor', 'redactor', 'epiceditor', 'ckeditor', 'default', 'froala', 'medium', 'summernote'])]
DJANGO_FRONT_EXTRA_CONTAINER_CLASSES = getattr(settings, 'DJANGO_FRONT_EXTRA_CONTAINER_CLASSES', '')
