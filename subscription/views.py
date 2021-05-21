import stripe

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView, View

from subscription.models import Customer, Product

stripe.api_key = settings.STRIPE_SECRET_KEY


class StripeConfiguration(LoginRequiredMixin, View):
    """
    Get the sesssion id based on Stripe primary key.
    """

    def get(self, request):
        stripe_config = {"publicKey": settings.STRIPE_PUBLISHABLE_KEY}
        context = JsonResponse(stripe_config, safe=False)
        return HttpResponse(context)


class CreateCheckoutSessionView(LoginRequiredMixin, View):
    """
    Create the checkout session for the subscription.
    """

    def get(self, request):
        domain_url = "http://localhost:8000/"
        try:
            checkout_session = stripe.checkout.Session.create(
                client_reference_id=request.user.id,
                success_url=domain_url + "success?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=domain_url + "cancel/",
                payment_method_types=["card"],
                mode="subscription",
                subscription_data={"trial_period_days": 7},
                line_items=[{"price": settings.STRIPE_PRICE_ID, "quantity": 1}],
            )
            context = JsonResponse({"sessionId": checkout_session["id"]})

        except Exception as e:
            context = JsonResponse({"error": str(e)})
        return HttpResponse(context)


class SuccessView(View):
    """
    Get the Success checkout for the subscription.
    """

    def get(self, request):
        # Fetch session id
        session = stripe.checkout.Session.retrieve(request.GET["session_id"])
        # Get the Stripe subscription
        subscription = stripe.Subscription.retrieve(session.subscription)
        # Get the Stripe Product
        plan = stripe.Product.retrieve(subscription.plan.product)
        try:
            # Get the product if its plan exist
            product = Product.objects.get(product_id=plan.id)
        except Product.DoesNotExist:
            # Create a product if doesn't exist
            product = Product.objects.create(
                name=plan.name,
                description=plan.description,
                price=subscription.plan.amount,
                currency=subscription.plan.currency,
                product_id=plan.id,
            )
        # Get the user and create a new Customer
        customer = Customer.objects.create(
            user=request.user,
            customer_id=session.customer,
            subscription_id=session.subscription,
            plan=product,
        )
        return render(request, "subscription/success.html")


class CancelView(TemplateView):
    """
    Get the cancel checkout of the subscription.
    """

    template_name = "subscription/cancel.html"


class SubscriptionCancelView(LoginRequiredMixin, View):
    """
    Cancel the Subscription if the subscription has been done.
    """

    def get(self, request):
        try:
            # Get the customer subscription id
            sub_id = request.user.customer.subscription_id if request.user else ""
            # Delete the Subscription from the Stripe
            stripe.Subscription.delete(sub_id)
            # Delete the Customer instance
            instance = Customer.objects.get(subscription_id=sub_id)
            instance.delete()
            message = "Your Subscription has been deleted !"
        except Exception as e:
            message = "Your subscription is not active !"

        context = {"message": message}
        return render(
            request, "subscription/check_active_subscription.html", context=context
        )


class StripeWebhook(LoginRequiredMixin, View):
    """
    Get the trigger event occurs in the subscription and update its details on stripe webhook.
    """

    def get(self, request):
        payload = request.body
        sig_header = request.META["HTTP_STRIPE_SIGNATURE"]

        event = None

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_ENDPOINT_SECRET
            )
        except ValueError as e:
            # Invalid payload
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            return HttpResponse(status=400)
        # Handle the checkout.session.completed event
        if event["type"] == "checkout.session.completed":
            session = event["data"]["object"]

            return HttpResponse(status=200)
        return HttpResponse(status=200)
