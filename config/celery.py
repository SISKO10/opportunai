import os
from celery import Celery

# On indique à Celery où trouver les settings Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# On crée l'application Celery
app = Celery('opportunai')

# On charge la configuration depuis les settings Django
# namespace='CELERY' signifie que toutes les configs
# Celery dans settings.py commencent par CELERY_
app.config_from_object('django.conf:settings', namespace='CELERY')

# Celery découvre automatiquement les tâches dans
# tous les fichiers tasks.py de chaque application
app.autodiscover_tasks()
