from django.contrib import admin

from .models import Checkout, CheckoutLine

# Register your models here.


admin.site.register(Checkout)
admin.site.register(CheckoutLine)