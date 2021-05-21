from django.views.generic.base import TemplateView
import stripe

from django.conf import settings
from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.views import LogoutView, LoginView
from django_registration.backends.one_step.views import RegistrationView

from subscription.models import Customer

stripe.api_key = settings.STRIPE_SECRET_KEY


class Login(LoginView):
    template_name = "core/registration/login.html"


class Logout(LogoutView):
    template_name = "core/registration/logout.html"


class RegisterView(RegistrationView):
    template_name = "core/django_registration/signup.html"
    success_url = "complete"


class RegistrationCompleteView(RegistrationView):
    template_name = "core/django_registration/signup_complete.html"


class HomeView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, *args, **kwargs):
        context = super(HomeView, self).get_context_data(*args, **kwargs)

        if self.request.user.is_authenticated:
            try:
                # Retrieve the customer, subscription & product
                customer = (
                    Customer.objects.get(user=self.request.user)
                    if self.request.user
                    else None
                )
                subscription = (
                    stripe.Subscription.retrieve(customer.subscription_id)
                    if customer
                    else ""
                )
                product = customer.plan if customer else ""
            except Customer.DoesNotExist:
                subscription = ""
                product = ""
            # Get the context
            context["subscription"] = subscription
            context["product"] = product

            return context
        else:
            return None
