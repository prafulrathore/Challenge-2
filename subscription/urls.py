from django.urls import path

from subscription import views

urlpatterns = [
    path('config/', views.StripeConfiguration.as_view(), name='config'),
    path('create-checkout-session/', views.CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('success/', views.SuccessView.as_view(), name='suceess'),
    path('cancel/', views.CancelView.as_view(), name='cancel'),
    path('cancelled/', views.SubscriptionCancelView.as_view(), name='cancelled'),
    path('webhook/', views.StripeWebhook.as_view(), name='webhook'),
]
