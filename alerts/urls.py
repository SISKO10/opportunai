from django.urls import path
from .views import alertes_view, supprimer_alerte_view

urlpatterns = [
    path('alertes/', alertes_view, name='alertes'),
    path('alertes/supprimer/<int:pk>/', supprimer_alerte_view, name='supprimer-alerte'),
]
