from django.urls import path

from core import views


urlpatterns = [
    path("signup/", views.RegisterView.as_view(), name="signup"),
    path(
        "signup/complete/",
        views.RegistrationCompleteView.as_view(),
        name="signup_complete",
    ),
    path("login/", views.Login.as_view(), name="login"),
    path("logout/", views.Logout.as_view(), name="logout"),
    path("", views.HomeView.as_view(), name="home"),
]
