from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    stripe_id = models.CharField(max_length=255)
    stripe_subscription_id = models.CharField(max_length=400)

    class meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

    def __str__(self):
        return f"{self.user.username}"


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=100, default="")
    price = models.FloatField()
    currency = models.CharField(max_length=10, default="")
    subscription_id = models.CharField(max_length=400, default="")

    class meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def save(self, *args, **kwargs):
        self.price = self.price / 100
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return f"Price of {self.name} is {self.price} {self.currency}"
