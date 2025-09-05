import os
from pathlib import Path

# Django settings for macnamer project.
from . import settings_import

DISPLAY_NAME = settings_import.DISPLAY_NAME

DEBUG = settings_import.DEBUG
TEMPLATE_DEBUG = DEBUG

BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.pardir))

ADMINS = (
)

MANAGERS = settings_import.ADMINS

ALLOWED_HOSTS = settings_import.ALLOWED_HOSTS

SECRET_KEY = settings_import.SECRET_KEY

CSRF_TRUSTED_ORIGINS = settings_import.CSRF_TRUSTED_ORIGINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',              # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.join(PROJECT_DIR, 'db/macnamer.db'), # Or path to database file if using sqlite3.
        'USER': '',                                          # Not used with sqlite3.
        'PASSWORD': '',                                      # Not used with sqlite3.
        'HOST': '',                                          # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                                          # Set to empty string for default. Not used with sqlite3.
    }
}

# PG Database
host = None
port = None

if 'DB_USER' in os.environ:
    if 'DB_HOST' in os.environ:
        host = os.environ.get('DB_HOST')
        port = os.environ.get('DB_PORT', '5432')

    elif 'DB_PORT_5432_TCP_ADDR' in os.environ:
        host = os.environ.get('DB_PORT_5432_TCP_ADDR')
        port = os.environ.get('DB_PORT_5432_TCP_PORT', '5432')

    else:
        host = 'db'
        port = '5432'

if host and port:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ['DB_NAME'],
            'USER': os.environ['DB_USER'],
            'PASSWORD': os.environ['DB_PASS'],
            'HOST': host,
            'PORT': port,
        }
    }

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

TIME_ZONE = settings_import.TIME_ZONE

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
# deprecated in Django 1.4, but django_wsgiserver still looks for it
# when serving admin media
ADMIN_MEDIA_PREFIX = '/static_admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_DIR, 'site_static'),
)

LOGIN_URL='/login/'
LOGIN_REDIRECT_URL='/'
LOGOUT_REDIRECT_URL = '/'

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
                'macnamer.context_processors.app_version',
                'macnamer.context_processors.django_version',
                'macnamer.context_processors.display_name',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

MIDDLEWARE = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'macnamer.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'macnamer.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_DIR, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'rest_framework',
    'rest_framework_api_key',
    'drf_spectacular',
    'namer',
    'django_bootstrap5',
    'health_check',
    'health_check.db',
    'health_check.storage',
    'health_check.contrib.migrations',
)

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Macnamer API',
    'DESCRIPTION': 'Gives a unique name to endpoints based on their serialnumber',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

if os.environ.get('SAML_ROOT_URL') and os.environ.get('SAML_SIGNIN_URL') and os.environ.get('SAML_SIGNOUT_URL') and os.environ.get('SAML_IDP_IDENTIFIER') and os.environ.get('SAML_METADATA_URL'):
    SAML_SESSION_COOKIE_NAME = 'saml_session'
    import saml2
    from saml2.saml import NAMEID_FORMAT_PERSISTENT
    AUTHENTICATION_BACKENDS += ('djangosaml2.backends.Saml2Backend',)
    INSTALLED_APPS += ['djangosaml2']
    MIDDLEWARE.append('djangosaml2.middleware.SamlSessionMiddleware')
    LOGIN_URL = '/saml2/login/'
    SAML_CONFIG = {
    'xmlsec_binary': '/usr/bin/xmlsec1',
    'entityid': '%s/saml2/metadata/' % os.environ['SAML_ROOT_URL'],
    'attribute_map_dir': os.path.join(BASE_DIR, 'attributemaps'),
    'allow_unknown_attributes': True,
    'service': {
        'sp' : {
            'authn_requests_signed': False,
            "allow_unsolicited": True,
            'want_assertions_signed': True,
            'want_response_signed': False,
            'allow_unknown_attributes': True,
            'name': 'Federated Django SP',
            'name_id_format': NAMEID_FORMAT_PERSISTENT,
            'endpoints': {
                'assertion_consumer_service': [
                    ('%s/saml2/acs/' % os.environ['SAML_ROOT_URL'],
                    saml2.BINDING_HTTP_POST),
                    ],
                'single_logout_service': [
                    ('%s/saml2/ls/' % os.environ['SAML_ROOT_URL'],
                    saml2.BINDING_HTTP_REDIRECT),

                    ('%s/saml2/ls/post' % os.environ['SAML_ROOT_URL'],
                    saml2.BINDING_HTTP_POST),
                    ],
                },
            'required_attributes': ['uid'],
            'idp': {
                '%sa' % os.environ['SAML_IDP_IDENTIFIER']: {
                    'single_sign_on_service': {
                        saml2.BINDING_HTTP_REDIRECT: '%s' % os.environ['SAML_SIGNIN_URL'],
                        },
                    'single_logout_service': {
                        saml2.BINDING_HTTP_REDIRECT: '%s' % os.environ['SAML_SIGNOUT_URL'],
                        },
                    },
                },
            },
        },
    'metadata': {
        'local': [os.path.join(BASE_DIR, 'metadata.xml')],
        'remote': [{"url": "%s" % os.environ['SAML_METADATA_URL']},],
        },
    'debug': 1,
    'valid_for': 24,
    }
else:
     LOGIN_URL='/login/'