from django.db import models
from django.contrib.auth import get_user_model
from uuid import uuid4


# Create your models here.

class Checkout(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(
        get_user_model(),
        on_delete = models.CASCADE, 
        blank= True,
        null = True, 
    )
    
    email = models.EmailField()
    token = models.UUIDField(
        primary_key = True,
        default = uuid4,
        editable = False    
    )
    
    note = models.TextField()
    
    #shipping not shipping_id
    shipping = models.ForeignKey('userprofile.Addresses',on_delete = models.CASCADE, blank= True, null=True)
    
    def __str__(self):
        return str(self.token)
    
    

class CheckoutLine(models.Model):
    checkout = models.ForeignKey(
        'Checkout', on_delete=models.CASCADE
    )
    
    product = models.ForeignKey(
        'product.Product', on_delete=models.CASCADE
    )
    
    quantity = models.PositiveIntegerField()
    
    def __str__(self):
        return self.product.name
    
    
    def get_sub_total(self):
        return round(self.product.price * self.quantity, 2)
    
    

