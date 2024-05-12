"""
ASGI config for a project.
"""
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
os.environ.setdefault('DJANGO_CONFIGURATION', 'Local')

from configurations.asgi import get_asgi_application  # noqa

application = get_asgi_application()
