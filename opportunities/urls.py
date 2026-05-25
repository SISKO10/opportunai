from django.urls import path
from .views import (
    CategoryListView,
    SourceListView,
    OpportunityListView,
    OpportunityDetailView,
    OpportunityTopView,
    AlertCreateView,
    opportunite_list,
    opportunite_detail,
)

urlpatterns = [

    # /api/categories/
    path('categories/', CategoryListView.as_view(), name='categories'),

    # /api/sources/
    path('sources/', SourceListView.as_view(), name='sources'),

    # /api/opportunites/
    path('opportunites/', OpportunityListView.as_view(), name='opportunites'),

    # /api/opportunites/top/
    # IMPORTANT : top/ doit être avant <int:pk>/
    # sinon Django interpréterait "top" comme un pk
    path('opportunites/top/', OpportunityTopView.as_view(), name='opportunites-top'),

    # /api/opportunites/1/
    path('opportunites/<int:pk>/', OpportunityDetailView.as_view(), name='opportunite-detail'),

    # /api/alertes/
    path('alertes/', AlertCreateView.as_view(), name='alertes'),

    # URLs Web
    path('opportunites/', opportunite_list, name='opportunite-list'),
    path('opportunites/<int:pk>/', opportunite_detail, name='opportunite-detail-web'),
]
