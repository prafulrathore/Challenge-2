from django.urls import path, include
from django_registration.backends.one_step.views import RegistrationView
from django.contrib.auth.views import LogoutView, LoginView
from users.views import home

urlpatterns = [
    path('accounts/register/', RegistrationView.as_view(), name='django_registration_register'),
    path('accounts/', include('django_registration.backends.one_step.urls')),
    path('accounts/login/', LoginView.as_view(template_name='django_registration/login.html'), name='login'), 
    path('accounts/logout/', LogoutView.as_view(template_name='django_registration/logout.html'), name='logout'), 
    path('', home, name='home')

]