from django.urls import path, include

from core import views

# app_name = "core"

urlpatterns = [
    path("signup/", views.RegisterView.as_view(), name="signup"),
    path(
        "signup/complete/",
        views.RegistrationCompleteView.as_view(),
        name="signup_complete",
    ),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", views.HomeView.as_view(), name="home"),
]
