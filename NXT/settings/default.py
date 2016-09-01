"""
Django settings for NXT project.

Generated by 'django-admin startproject' using Django 1.8.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from django.utils.translation import ugettext_lazy as _

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*u7icc*h6*sj2ef#6lwphzr=*a2wbbz7m#=3wrtaz0viz#g(aj'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'bootstrap3',
    'django_admin_bootstrapped',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.flatpages',
    'tinymce',
    'mail_templated',
    'compressor',
    'ensomus',
    'common',
    'corsheaders',
    'django_mailer_plus'
)

#CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = ('enso-dev.chisw.us', 'nxtlvl-dev.chisw.us', 'localhost:3000', '127.0.0.1:3000')
CORS_ALLOW_METHODS = ('GET', 'POST', 'OPTIONS')
CORS_ALLOW_HEADERS = (
    'DNT','X-CustomHeader','Keep-Alive','User-Agent','X-Requested-With','If-Modified-Since',
    'Cache-Control','Content-Type','Accept-Encoding','Accept-Language', 'X-CSRFToken'
)
CORS_ALLOW_CREDENTIALS = True



MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'django.middleware.security.SecurityMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    # 'firepython.middleware.FirePythonDjango',
    'threadlocals.middleware.ThreadLocalMiddleware',
    'NXT.middleware.exceptions_middleware.ConvertExceptionMiddleware',
)

ROOT_URLCONF = 'NXT.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), os.path.join(BASE_DIR, 'nxtlvl_js/dist')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.static',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'NXT.wsgi.application'


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'da'

LANGUAGES = (
    ('da', _('Danish')),
    ('en', _('English'))
)

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Copenhagen'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/djstatic/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'commonstatic')

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'compressor.finders.CompressorFinder'
)

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
    # os.path.join(BASE_DIR, "nxtlvl_js/dist"),
)


# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    # 'django.template.loaders.eggs.Loader',
)


TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.contrib.messages.context_processors.messages",
    'django.core.context_processors.request'

)


TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, 'templates'),
)

SITE_ID = 1


# TinyMCE

# TINYMCE_JS_URL = os.path.join(MEDIA_URL, "tiny_mce/tiny_mce.js")
# TINYMCE_JS_ROOT = os.path.join(MEDIA_ROOT, "tiny_mce")

TINYMCE_COMPRESSOR = False

TINYMCE_DEFAULT_CONFIG = {

    'theme': "advanced",

}


# Project var

ADMINS = (
    # ('Johs Kristoffersen', 'johsbk@gmail.com'),
    ('Tim Lund', 'tl@t3cms.dk'),
)
MANAGERS = ADMINS


FILES_ROOT = os.path.join(BASE_DIR, 'files')


LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)


# GROUPS = {
#     {'name': 'Enso-bruger', 'rank': 1},
#     {'name': 'Firma-superbruger', 'rank': 2},
#     {'name': 'Leder', 'rank': 3},
#     {'name': 'Medarbejder', 'rank': 4}
# }


# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True


# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# This is only used where it's absolutely needed, like pdf templates.
SITE_URL = 'http://localhost:8000'

AUTHENTICATION_BACKENDS = ['ensomus.views.EmailAuthBackend']


AUTH_USER_MODEL = 'ensomus.UserNxtlvl'

# STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
if os.getenv('COOKIE_DOMAIN'):
    CSRF_COOKIE_DOMAIN = os.getenv('COOKIE_DOMAIN', 'localhost')
    SESSION_COOKIE_DOMAIN = os.getenv('COOKIE_DOMAIN', 'localhost')

# celery config

BROKER_URL = os.getenv('REDISCLOUD_URL', 'redis://')
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT=['json']
CELERY_TIMEZONE = 'Europe/Kiev'
CELERY_ENABLE_UTC = True

SEND_MAIL_REDIS_LOCK_KEY = 'send_mail_lock'