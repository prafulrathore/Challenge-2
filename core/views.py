import stripe

from django.conf import settings
from django.views.generic.base import TemplateView

from django_registration.backends.one_step.views import RegistrationView

from subscription.models import Subscription

stripe.api_key = settings.STRIPE_SECRET_KEY


class RegisterView(RegistrationView):
    template_name = "core/django_registration/signup.html"
    success_url = "complete"


class RegistrationCompleteView(RegistrationView):
    template_name = "core/django_registration/signup_complete.html"


class HomeView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, *args, **kwargs):
        context = super(HomeView, self).get_context_data(*args, **kwargs)

        try:
            # Retrieve the customer, subscription & product
            product = (
                Subscription.objects.get(user=self.request.user)
                if self.request.user
                else None
            )
            subscription = (
                stripe.Subscription.retrieve(product.subscription_id) if product else ""
            )
        except Subscription.DoesNotExist:
            subscription = ""
            product = ""
        # Get the context
        context["subscription"] = subscription
        context["product"] = product

        return context
