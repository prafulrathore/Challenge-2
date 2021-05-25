from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    product_name = models.CharField(max_length=256, default="")
    product_description = models.CharField(max_length=256, default="")
    product_price = models.FloatField(default=0)
    product_currency = models.CharField(max_length=256, default="")
    product_id = models.CharField(max_length=256, default="")

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.name}"


class Subscription(Product):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    customer_id = models.CharField(max_length=256, default="")
    subscription_id = models.CharField(max_length=256, default="")

    class Meta:
        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"

    def __str__(self):
        return f"{self.user.username}"

    def save(self, *args, **kwargs):
        self.product_price = self.product_price / 100
        super(Product, self).save(*args, **kwargs)
