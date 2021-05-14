from django.contrib import admin

# Register your models here.
from .models import StripeCustomer


admin.site.register(StripeCustomer)