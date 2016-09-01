from .default import *


ALLOWED_HOSTS = ["*"]


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'nxtlvl',
        'USER': 'root',
        'PASSWORD': 'root',
    }
}


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {

    'version': 1,

    'disable_existing_loggers': False,

    'formatters': {

        'verbose': {

            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'

        },

        'simple': {

            'format': '%(levelname)s %(message)s'

        },

    },

    'filters': {

        'require_debug_false': {

            '()': 'django.utils.log.RequireDebugFalse'

        }

    },

    'handlers': {

        'mail_admins': {

            'level': 'ERROR',

            'filters': ['require_debug_false'],

            'class': 'django.utils.log.AdminEmailHandler',

            'formatter': 'verbose'

        },

        'console': {

            # logging handler that outputs log messages to terminal

            'class': 'logging.StreamHandler',

            'level': 'DEBUG',  # message level to be written to console

            'formatter': 'verbose'

        },

        'file': {

            'class': 'logging.FileHandler',

            'filename': os.path.join(BASE_DIR, 'log', 'app.log'),

            'level': 'DEBUG',

            'formatter': 'verbose'

        },

    },

    'loggers': {

        'django.request': {

            'handlers': ['console', 'file'],

            'level': 'DEBUG',

            'propagate': True,

        },

        'django_mailer_plus': {

            'handlers': ['console'],

            'level': 'ERROR',

            'propagate': True,

        },

        'ho.pisa': {

            'handlers': ['console'],

            'level': 'ERROR',

            'propagate': True,

        },

        'django.db': {

            'handlers': ['console'],

            'level': 'ERROR',

            'propagate': True,

        },


        'ensomus': {

            'handlers': ['file', 'console'],

            'level': 'DEBUG',


            'propagate': True,

        },


        # 'django.db': {

        # 'handlers': ['console'],

        #     'level' : 'DEBUG'

        # },

    }

}


# EMAIL_HOST = ''
#
# EMAIL_HOST_USER = ''
#
# EMAIL_HOST_PASSWORD = ''
#
# EMAIL_PORT = 587

# EMAIL_HOST = 'smtp.webfaction.com'
# EMAIL_HOST_USER = 'enso'
# EMAIL_HOST_PASSWORD = 'hsi(8ujIKl'
# EMAIL_PORT = 587
#
# SERVER_EMAIL = DEFAULT_FROM_MAIL
#
# DEFAULT_FROM_EMAIL = DEFAULT_FROM_MAIL
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
DEFAULT_FROM_EMAIL = 'kharenko.send.mail@gmail.com'
EMAIL_HOST_USER = 'kharenko.send.mail@gmail.com'
EMAIL_HOST_PASSWORD = '^Work1029Send$'
EMAIL_PORT = 587
EMAIL_TIMEOUT = 300

DEBUG = False
