from django.urls import path,include
from .views import RegistrationView, LoginView
# from .views import CustomLoginView



urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    # path('custom-token/', CustomLoginView.as_view(), name='custom_token'),
]
