from django.conf import settings

DJANGO_FRONT_PERMISSION = getattr(settings, 'DJANGO_FRONT_PERMISSION', lambda u: u and u.is_staff)
