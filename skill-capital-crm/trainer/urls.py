from django.urls import path
from .views import TrainerCreateView

urlpatterns = [
    path('trainers/', TrainerCreateView.as_view(), name='create_trainer_api'),
]
