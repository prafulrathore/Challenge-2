import stripe

from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView, View

from .models import StripeCustomer


class SuccessView(TemplateView):
    template_name = "subscription/success.html"


class CancelView(TemplateView):
    template_name = "subscription/cancel_checkout.html"


class StripeConfiguration(View):
    def get(self, request):
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        context = JsonResponse(stripe_config, safe=False)
        return HttpResponse(context)


class CreateCheckoutSessionView(View):
    def get( request):
        if request.method == 'GET':
            domain_url = 'http://localhost:8000/'
            stripe.api_key = settings.STRIPE_SECRET_KEY
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
                    ]

                )
                context = JsonResponse({'sessionId': checkout_session['id']})

            except Exception as e:
                context = JsonResponse({'error': str(e)})
            return HttpResponse(context)


class SubscriptionCancelView(TemplateView):
    template_name = "subscription/cancelled.html"


class CancelledView(View):
    def get(self, request):
        if request.user.is_authenticated:
            sub_id = request.user.subscription.id

            stripe.api_key = settings.STRIPE_SECRET_KEY

            try:
                stripe.Subscription.delete(sub_id)
            except Exception as e:
                context = JsonResponse({'error': (e.args[0])}, status=403)
                return HttpResponse(context)

        return redirect("home.html")


class StripeWebhook(View):
    def get(self, request):
        stripe.api_key = settings.STRIPE_SECRET_KEY
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

            # Fetch all the required data from session
            client_reference_id = session.get('client_reference_id')
            stripe_customer_id = session.get('customer')
            stripe_subscription_id = session.get('subscription')

            # Get the user and create a new StripeCustomer
            user = User.objects.get(id=client_reference_id)
            StripeCustomer.objects.create(
                user=user,
                stripeCustomerId=stripe_customer_id,
                stripeSubscriptionId=stripe_subscription_id,
            )
            print(user.username + ' just subscribed.')

        return HttpResponse(status=200)
