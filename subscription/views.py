import stripe

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, View

from subscription.models import Customer, Product

stripe.api_key = settings.STRIPE_SECRET_KEY


class StripeConfiguration(View):
    def get(self, request):
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        context = JsonResponse(stripe_config, safe=False)
        return HttpResponse(context)


class CreateCheckoutSessionView(View):
    def get(self, request):
        domain_url = 'http://localhost:8000/'
        try:
            checkout_session = stripe.checkout.Session.create(
                client_reference_id=request.user.id if request.user.is_authenticated else None,
                success_url=domain_url +
                'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancel/',
                payment_method_types=['card'],
                mode='subscription',
                subscription_data={'trial_period_days': 7},
                line_items=[
                    {
                        'price': settings.STRIPE_PRICE_ID,
                        'quantity': 1,
                    }
                ],
            )
            context = JsonResponse({'sessionId': checkout_session['id']})

        except Exception as e:
            context = JsonResponse({'error': str(e)})
        return HttpResponse(context)


class SuccessView(View):
    def get(self, request):
        # Fetch session id
        session = stripe.checkout.Session.retrieve(request.GET['session_id'])
        # Get the user and create a new StripeCustomer
        customer = Customer()
        customer.user = request.user
        customer.stripe_id = session.customer
        customer.stripe_subscription_id = session.subscription
        customer.save()
        # Create a product
        product = Product()
        subscription = stripe.Subscription.retrieve(
            customer.stripe_subscription_id)
        plan = stripe.Product.retrieve(subscription.plan.product)
        product.name = plan.name
        product.description = plan.description
        product.price = subscription.plan.amount
        product.currency = subscription.plan.currency
        product.subscription_id = session.subscription
        product.save()
        return render(request, 'subscription/success.html')


class CancelView(TemplateView):
    template_name = "subscription/cancel.html"


class SubscriptionCancelView(View):
    def get(self, request):
        if request.user.is_authenticated:
            try:
                sub_id = request.user.customer.stripe_subscription_id if Customer else ""
                stripe.Subscription.delete(sub_id)
                Customer.objects.filter(stripe_subscription_id=sub_id).delete()
                Product.objects.filter(subscription_id=sub_id).delete()
                message = "Your Subscription has been deleted !"
            except Exception as e:
                message = "Your subscription is not active !"

        context = {'message': message}
        return render(request, 'subscription/check_active_subscription.html', context=context)


class StripeWebhook(View):
    def get(self, request):
        endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']

        event = None

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header,  endpoint_secret
            )
        except ValueError as e:
            # Invalid payload
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            return HttpResponse(status=400)
        # Handle the checkout.session.completed event
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']

            return HttpResponse(status=200)
        return HttpResponse(status=200)
