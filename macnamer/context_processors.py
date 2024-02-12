import django
from django.conf import settings
from .utils import get_server_version

APP_VERSION = get_server_version()

def display_name(request):
    return {'DISPLAY_NAME': settings.DISPLAY_NAME}

def config_installed(request):
    return {'CONFIG_INSTALLED': True if 'config' in settings.INSTALLED_APPS else False}

def app_version(request):
    return {'APP_VERSION': APP_VERSION}

def django_version(request):
    return { 'DJANGO_VERSION': django.get_version() }