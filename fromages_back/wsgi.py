"""
WSGI config for fromages_back project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fromages_back.settings')
os.environ.setdefault('PORT', '10000')  # Render usa 10000 por defecto
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fromages_back.settings')

application = get_wsgi_application()
