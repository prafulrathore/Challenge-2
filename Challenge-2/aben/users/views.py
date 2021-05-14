import stripe
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings
from strip_app.models import StripeCustomer
# Create your views here.

@login_required
def home(request):
    try:
        # Retrieve the subscription & product
        user = request.user
        stripe_customer = StripeCustomer.objects.get(user=user)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        subscription = stripe.Subscription.retrieve(stripe_customer.stripeSubscriptionId)
        product = stripe.Product.retrieve(subscription.plan.product)

        # Feel free to fetch any additional data from 'subscription' or 'product'
        # https://stripe.com/docs/api/subscriptions/object
        # https://stripe.com/docs/api/products/object

        return render(request, 'home.html', {
            'subscription': subscription,
            'product': product,
        })

    except StripeCustomer.DoesNotExist:
        return render(request, 'home.html')