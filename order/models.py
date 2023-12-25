from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

order_status = ((0, "Fullfield"), (1, "Unfullfield"), (2, "Canceled"), (3, "Refunded"))

class Order(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=order_status, default=0)
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    email = models.EmailField()
    checkout_token = models.CharField(max_length=36, default="")
    note = models.TextField(blank=True, default="")
    shipping = models.ForeignKey('userprofile.Addresses',on_delete = models.CASCADE)
    total = models.FloatField()
    
    def __str__(self):
        return self.email
    
    
class OrderLine(models.Model):
    order = models.ForeignKey(
        Order, on_delete = models.CASCADE,
        #editable=False,
        related_name = "orderlines", #
    )
    
    product = models.ForeignKey(
        'product.Product', 
        on_delete =  models.SET_NULL,
        blank = True,
        null = True,
        related_name = "orderlines"
    )
    
    product_name = models.CharField(max_length = 255)
    product_price = models.FloatField()
    sku = models.CharField(max_length = 50)
    quantity = models.PositiveIntegerField()
    
    def __str__(self):
        return f"{self.product_name}x{self.product_price}"
    
    def get_sub_total(self):
        return round(self.product_price * self.quantity, 2)
    