#!/usr/bin/python
from os import getenv
import locale

# Read list of admins from $MACNAMER_ADMINS env var
admin_list = []
if getenv('MACNAMER_ADMINS'):
    admins_var = getenv('MACNAMER_ADMINS')
    if ',' in admins_var and ':' in admins_var:
        for admin in admins_var.split(':'):
            admin_list.append(tuple(admin.split(',')))
        ADMINS = tuple(admin_list)
    elif ',' in admins_var:
        admin_list.append(tuple(admins_var.split(',')))
        ADMINS = tuple(admin_list)
else:
    ADMINS = (
                ('Admin User', 'admin@test.com')
             )

# Read the preferred time zone from $MACNAMER_TZ, use system locale or
# set to 'America/Chicago' if neither are set
if getenv('MACNAMER_TZ'):
    if '/' in getenv('MACNAMER_TZ'):
        TIME_ZONE = getenv('MACNAMER_TZ')
    else: TIME_ZONE = 'America/Chicago'
elif getenv('TZ'):
    TIME_ZONE = getenv('TZ')
else:
    TIME_ZONE = 'America/Chicago'

# Read the preferred language code from $MACNAMER_LANG, use system locale or
# set to 'en_US' if neither are set
if getenv('MACNAMER_LANG'):
    if '_' in getenv('MACNAMER_LANG'):
        LANGUAGE_CODE = getenv('MACNAMER_LANG')
    else:
        LANGUAGE_CODE = 'en_US'
# elif locale.getdefaultlocale():
#     LANGUAGE_CODE = locale.getdefaultlocale()[0]
else:
    LANGUAGE_CODE = 'en_US'

# Read the list of allowed hosts from the $DOCKER_MACNAMER_ALLOWED env var, or
# allow all hosts if none was set.
if getenv('DOCKER_MACNAMER_ALLOWED'):
    ALLOWED_HOSTS = getenv('DOCKER_MACNAMER_ALLOWED').split(',')
else:
    ALLOWED_HOSTS = ['*']

# Set the display name from the $DOCKER_MACNAMER_DISPLAY_NAME env var, or
# use the default
if getenv('DOCKER_MACNAMER_DISPLAY_NAME'):
    DISPLAY_NAME = getenv('DOCKER_MACNAMER_DISPLAY_NAME')
else:
    DISPLAY_NAME = 'Macnamer'


# Read secret key from the $SECRET_KEY env var, or
# set a default one
if getenv('SECRET_KEY'):
    SECRET_KEY = getenv('SECRET_KEY')
else:
    SECRET_KEY = ['2&lakkwf+r78)9u+30&+1=zc3()1^s2oqrbxr5qe8z_@xm2a&4']

# Setting HOST_NAME might be needed depending on loadbalancers and ingests
if getenv("HOST_NAME"):
    HOST_NAME = getenv("HOST_NAME")
    CSRF_TRUSTED_ORIGINS = [getenv("HOST_NAME")]
else:
    HOST_NAME = "http://localhost"
    CSRF_TRUSTED_ORIGINS = []

# Read the DEBUG setting from env var
try:
    if getenv('DOCKER_MACNAMER_DEBUG').lower() == 'true':
        DEBUG = True
    else:
        DEBUG = False
except Exception:
    DEBUG = False