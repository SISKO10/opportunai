
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

# URLs API (sans login_required)
api_urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('sources/', SourceListView.as_view(), name='sources'),
    path('opportunites/', OpportunityListView.as_view(), name='opportunites'),
    path('opportunites/top/', OpportunityTopView.as_view(), name='opportunites-top'),
    path('opportunites/<int:pk>/', OpportunityDetailView.as_view(), name='opportunite-detail'),
    path('alertes/', AlertCreateView.as_view(), name='alertes'),
]

# URLs Web (avec login_required)
urlpatterns = [
    path('opportunites/', opportunite_list, name='opportunite-list'),
    path('opportunites/<int:pk>/', opportunite_detail, name='opportunite-detail-web'),
]
