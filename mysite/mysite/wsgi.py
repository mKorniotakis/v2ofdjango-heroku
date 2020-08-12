"""
WSGI config for mysite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

# For integration with apache2.4 you should uncomment the next 3 commented lines

import os

from django.core.wsgi import get_wsgi_application

# For integration with apache2.4 you should uncomment the next 1 commented line

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

application = get_wsgi_application()
