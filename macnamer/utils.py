import os
import pathlib
import plistlib
from django.conf import settings

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.pardir))

def get_server_version():
    data = (pathlib.Path(PROJECT_DIR) / 'macnamer/version.plist').read_bytes()
    return plistlib.loads(data)['version']

def get_install_type():
    if os.path.exists('/home/docker'):
        return 'docker'
    else:
        return 'bare'

def get_django_setting(name, default=None):
    """Get a setting from the Django.conf.settings object"""
    return getattr(settings, name, default)