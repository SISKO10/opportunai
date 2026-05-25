"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Interface admin Django
    path('admin/', admin.site.urls),

    # Interface de test DRF
    path('api-auth/', include('rest_framework.urls')),

    # Toutes nos URLs API
    # prefixe "api/" devant chaque URL
    path('api/', include('opportunities.urls')),

    # Dashboard (page d'accueil)
    path('', include('dashboard.urls')),

    #Opportunites (listes et detail)
    path('', include('opportunities.urls')),
]
