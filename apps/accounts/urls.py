from rest_framework.urls import path
from .views import SignupView, LoginView

urlpatterns = [
    path("sign-up", SignupView.as_view(), name="sign-up"),
    path("login", LoginView.as_view(), name="login"),
]
