from django.db import models
from django.contrib.auth.models import User


class StripeCustomer(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=255)
    stripe_subscription_id = models.CharField(max_length=255)

    def __str__(self):
        return f"self.user.username"
