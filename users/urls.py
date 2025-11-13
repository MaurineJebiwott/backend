# users/urls.py
from django.urls import path
from .views import RegisterView, LoginView, CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, LoginView, current_user

urlpatterns = [
    path("api/token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"), 
    path("me/", current_user, name="current-user"), # optional
]

