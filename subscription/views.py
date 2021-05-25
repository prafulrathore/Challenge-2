import stripe

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView, View

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from subscription.models import Subscription

stripe.api_key = settings.STRIPE_SECRET_KEY


class StripeConfiguration(LoginRequiredMixin, View):
    """
    Get the sesssion id by stripe Publishable api key to identify user account
    """

    def get(self, request):
        stripe_config = {"publicKey": settings.STRIPE_PUBLISHABLE_KEY}
        context = JsonResponse(stripe_config, safe=False)
        return HttpResponse(context)


class CreateCheckoutSessionView(LoginRequiredMixin, APIView):
    """
    Create the checkout session for the subscription.
    """

    def get(self, request, format=None):
        protocol = request.is_secure() and "https" or "http"
        site = get_current_site(request)
        domain_url = f"{protocol}://{site}/"
        print(domain_url)
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
            context = {"sessionId": checkout_session["id"]}

        except Exception as e:
            context = {"error": str(e)}
        return Response(context)


class SuccessView(View):
    """
    Get the Success view if the subscription process have been completed.
    """

    def get(self, request):
        # Fetch session id
        session = stripe.checkout.Session.retrieve(request.GET["session_id"])
        # Get the Stripe subscription
        subscription = stripe.Subscription.retrieve(session.subscription)
        # Get the Stripe Product
        plan = stripe.Product.retrieve(subscription.plan.product)
        # Get the user and create a new Customer
        instance = Subscription.objects.create(
            product_name=plan.name,
            product_description=plan.description,
            product_price=subscription.plan.amount,
            product_currency=subscription.plan.currency,
            product_id=plan.id,
            user=request.user,
            customer_id=session.customer,
            subscription_id=session.subscription,
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
            sub_id = request.user.subscription.subscription_id if request.user else ""
            # Delete the Subscription from the Stripe
            stripe.Subscription.delete(sub_id)
            # Delete the Customer instance
            instance = Subscription.objects.get(subscription_id=sub_id)
            instance.delete()
            message = "Your Subscription has been deleted !"
        except Exception as e:
            message = "Your subscription is not active !"

        context = {"message": message}
        return render(
            request, "subscription/check_active_subscription.html", context=context
        )


class StripeWebhook(LoginRequiredMixin, APIView):
    """
    Get the trigger event that occurs in the subscription and update its details on stripe webhook.
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
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # Handle the checkout.session.completed event
        if event["type"] == "checkout.session.completed":
            session = event["data"]["object"]
            print(request.user.username + " just subscribed.")

            return Response(status=status.HTTP_200_OK)
        # Handle the customer.subscription.deleted event
        if event["type"] == "customer.subscription.deleted":
            print(request.user.username + "'s subscription deleted")
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_200_OK)
