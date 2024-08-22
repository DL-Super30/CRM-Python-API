from django.urls import path
from .views import LeadListCreate

urlpatterns = [
    path('api/getleads/', LeadListCreate.as_view(), name='lead-list-create'),
]
