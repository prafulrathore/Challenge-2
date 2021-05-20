import stripe

from django.conf import settings
from django.shortcuts import render
from django.views.generic import View

from subscription.models import Customer, Product

stripe.api_key = settings.STRIPE_SECRET_KEY


class HomeView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'core/home.html')
        else:
            try:
                # Retrieve the subscription & product
                customer = Customer.objects.get(user=request.user)
                subscription = stripe.Subscription.retrieve(
                    customer.stripe_subscription_id) if customer else ""
                product = Product.objects.get(
                    subscription_id=subscription.id) if subscription else ""
            except Customer.DoesNotExist:
                subscription = ""
                product = ""
            # Get the context
            context = {
                'subscription': subscription,
                'product': product,
            }
            return render(request, 'core/home.html', context)
