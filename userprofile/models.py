from django.db import models
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save
# from phone_field import PhoneField

User = get_user_model()

class Addresses(models.Model):
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    # phone = PhoneField(help_text='Contact phone number', blank=True, null=True)
    
    def __str__(self):
        return "{}|{}|{}|{}".format(self.street_address, self.city, 
                                    self.postal_code, self.phone)
    

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    
    user_addresses = models.ManyToManyField(Addresses)
    
    def __str__(self):
        return self.user.email
        
@receiver(post_save, sender=User)
def create_profile(instance, created, *args, **kwargs):
    
    if created:
        UserProfile.objects.create(user = instance)
        
    
