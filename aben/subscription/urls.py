from django.urls import path

from subscription.views import (SuccessView, CancelView, CancelledView, StripeConfiguration,
                                CreateCheckoutSessionView, SubscriptionCancelView, StripeWebhook)

urlpatterns = [
    path('config/', StripeConfiguration.as_view()),
    path('create-checkout-session/', CreateCheckoutSessionView.as_view()),
    path('success/', SuccessView.as_view()),
    path('cancel/', CancelView.as_view()),
    path("complete", SubscriptionCancelView.as_view(), name="complete"),
    path('cancelled/', CancelledView.as_view(), name='cancelled'),
    path('webhook/', StripeWebhook.as_view()),
]
