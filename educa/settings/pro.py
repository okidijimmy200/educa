# pro.py: Custom settings for the production environment
from .base import *

# DEBUG: Setting DEBUG to False should be mandatory for any production environment. Failing to do so will result in the traceback information and sensitive configuration data being exposed to everyone
DEBUG = False

# ADMINS: When DEBUG is False and a view raises an exception, all information will be sent by email to the people listed in the ADMINS setting. Make sure that you replace the name/email tuple with your own information
ADMINS = (
    ('jimmy', 'okidijimmie@gmail.com'),
)

# ALLOWED_HOSTS: Django will only allow the hosts included in this list to serve the application. This is a security measure. You include the asterisk symbol, *, to refer to all hostnames. You will limit the hostnames that can be used for serving the application later.
# ALLOWED_HOSTS = ['.educaproject.com']
ALLOWED_HOSTS = ['*']

DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.postgresql',
       'NAME': 'educa',
       'USER': 'postgres',
       'PASSWORD': '12345',
   }
}

# SSL config
# SECURE_SSL_REDIRECT = True
# CSRF_COOKIE_SECURE = True


