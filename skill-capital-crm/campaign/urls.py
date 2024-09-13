from django.urls import path
from .views import CampaignListCreateView

urlpatterns = [
    path('campaigns/', CampaignListCreateView.as_view(), name='campaign-list-create'),
]
