import datetime
import os
import sys
import traceback

PYTHON_EXE = '/usr/bin/python3'
if sys.executable != PYTHON_EXE:
    os.execl(PYTHON_EXE, PYTHON_EXE, *sys.argv)


def exceptionLoggingMiddleware(application, logfile):
    '''
    very basic exception logging middleware application which could be useful
    if you are able to get this module to run, but your app can not respond to
    requests for some reason and it is not able to log why.
    '''
    def logApp(environ, start_response):
        try:
            return application(environ, start_response)
        except:
            fh = open(logfile, 'a')
            fh.write(datetime.datetime.now().isoformat()+'\n'+traceback.format_exc())
            fh.close()
            raise
    return logApp
            

def moveEnvVarsWSGIMiddleware(application, keys):
    '''
    application: wsgi application that needs some env vars transferred.  
    keys: a list of environment variable names.
    wsgi middleware application that transfers environment variables from the
    wsgi environment to the os environment before calling application.
    '''
    def app(environ, start_response):
        for key in keys:
            if environ.has_key(key):
                os.environ[key] = environ[key]
        return application(environ, start_response)
    return app

sys.path.append(os.path.dirname(__file__))

MACNAMER_ENV_DIR = '/home/app/macnamer'

# Make sure we have the virtualenv and the Django app itself added to our path
sys.path.append(MACNAMER_ENV_DIR)
sys.path.append(os.path.join(MACNAMER_ENV_DIR, 'macnamer'))

import macnamer.wsgi
application = macnamer.wsgi.application
