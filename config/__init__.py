# On charge Celery dès que Django démarre
from .celery import app as celery_app

__all__ = ('celery_app',)
