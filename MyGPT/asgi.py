"""
ASGI config for MyGPT project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

# 接受网络请求 不需要修改 异步式

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MyGPT.settings')

application = get_asgi_application()
