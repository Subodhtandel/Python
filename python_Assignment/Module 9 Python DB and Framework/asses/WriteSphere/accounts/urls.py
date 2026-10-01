from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import LoginView, ProfileUpdateView, RegistrationView

urlpatterns = [
    path("signup/", RegistrationView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path(
        "logout/",
        LogoutView.as_view(next_page="blog:list"),
        name="logout",
    ),
    path("profile/edit/", ProfileUpdateView.as_view(), name="profile_edit"),
]
