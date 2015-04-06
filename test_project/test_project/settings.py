# Django settings for test_project project.
import os
DEBUG = True
TEMPLATE_DEBUG = DEBUG
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.path.dirname(__file__), 'test_project.db'),
    }
}

USE_I18N = True
USE_L10N = True
SECRET_KEY = 'lol I dont even care'


LANGUAGES = (
    ('en', 'en'),
    ('fr', 'fr'),
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware'  # needed for tests
)
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request'  # needed for tests
)
TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), '..', 'templates'), )
STATIC_URL = '/static/'

ROOT_URLCONF = 'test_project.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'test_project.wsgi.application'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',

    'front'
)

SITE_ID = 1
