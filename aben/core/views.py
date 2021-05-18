import stripe

from django.conf import settings
from django.shortcuts import render
from django.views.generic import View

from subscription.models import StripeCustomer


class HomeView(View):
    def get(self, request):
        try:
            # Retrieve the subscription & product
            user = request.user
            stripe_customer = StripeCustomer.objects.get(user=user)
            stripe.api_key = settings.STRIPE_SECRET_KEY
            subscription = stripe.Subscription.retrieve(
                stripe_customer.stripeSubscriptionId) if stripe_customer else ""
            product = stripe.Product.retrieve(
                subscription.plan.product) if subscrption else ""

        except StripeCustomer.DoesNotExist:
            subscription = ""
            product = ""
        # Get the context
        context = {
            'subscription': subscription,
            'product': product,
        }
        return render(request, 'core/home.html', context)
