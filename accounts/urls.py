from django.urls import path
from .views import (
    login_view,
    register_view,
    logout_view,
    profil_view,
    modifier_profil_view,
    changer_mot_de_passe_view,
)

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('profil/', profil_view, name='profil'),
    path('profil/modifier/', modifier_profil_view, name='modifier-profil'),
    path('profil/changer-mot-de-passe/', changer_mot_de_passe_view, name='changer-mot-de-passe'),
]
