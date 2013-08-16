from django.conf import settings

DJANGO_FRONT_PERMISSION = getattr(settings, 'DJANGO_FRONT_PERMISSION', lambda u: u and u.is_staff)
DJANGO_FRONT_EDIT_MODE = getattr(settings, 'DJANGO_FRONT_EDIT_MODE', 'lightbox')  # ('lightbox' or 'inline')
DJANGO_FRONT_EDITOR_OPTIONS = getattr(settings, 'DJANGO_FRONT_EDITOR_OPTIONS', dict())
