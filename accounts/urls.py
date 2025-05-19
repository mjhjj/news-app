from django.urls import path
from .views import signup_view, ProfileView, LogoutView

urlpatterns = [
    path("signup/", signup_view, name="signup"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("logoutASK/", LogoutView.as_view(), name="logoutASK"),
]
