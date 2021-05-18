from django.urls import path, include
from django_registration.backends.one_step.views import RegistrationView
from django.contrib.auth.views import LogoutView, LoginView
from django.urls import reverse_lazy

from core.views import HomeView

urlpatterns = [
    path('accounts/register/', RegistrationView.as_view(template_name="core/django_registration/registration_form.html"), name ='django_registration_register'),
    path('accounts/register/complete/', RegistrationView.as_view(template_name="core/django_registration/registration_complete.html"), name= 'django_registration_complete'),
    path('accounts/', include('django_registration.backends.one_step.urls')),
    path('accounts/login/', LoginView.as_view(template_name='core/django_registration/login.html'), name='login'), 
    path('accounts/logout/', LogoutView.as_view(template_name='core/django_registration/logout.html'), name='logout'), 
    path('', HomeView.as_view(), name='home')
]
