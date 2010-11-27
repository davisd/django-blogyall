"""
Settings defaults - settings should be overridden in the project's settings.py
"""
from django.conf import settings

DEBUG = getattr(settings, 'DEBUG', True)

BLOG_PING_GOOGLE = getattr(settings, 'BLOG_PING_GOOGLE', False)

BLOG_COMMENTS_EMAIL_NOTIFICATION = getattr(settings,
    'BLOG_COMMENTS_EMAIL_NOTIFICATION', False)

BLOG_COMMENTS_AUTO_MODERATE = getattr(settings,
    'BLOG_COMMENTS_AUTO_MODERATE', False)
BLOG_COMMENTS_MODERATE_AFTER = getattr(settings,
    'BLOG_COMMENTS_MODERATE_AFTER', None)

BLOG_COMMENTS_AUTO_CLOSE = getattr(settings, 'BLOG_COMMENTS_AUTO_CLOSE', False)
BLOG_COMMENTS_CLOSE_AFTER = getattr(settings, 'BLOG_COMMENTS_CLOSE_AFTER', None)
