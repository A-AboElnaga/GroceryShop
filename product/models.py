from django.db import models
from django.urls import reverse, reverse_lazy
from django.utils.text import slugify
from mptt.managers import TreeManager
from mptt.models import MPTTModel
from django_countries.fields import CountryField
import uuid

fields = ["name", "description", "background_image"]

# Create your models here.
class Category(MPTTModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField()
    background_image = models.ImageField(upload_to = 'category_background', 
                                         blank = True, null = True
    )
    parent = models.ForeignKey(
        'self', 
        blank = True,
        null = True, 
        on_delete = models.CASCADE
    )
    
    tree = TreeManager()
    
    def __str__(self):
        return self.name
    
    
    def get_absolute_url(self):
        return reverse_lazy("dashboard:category_dashboard:category_list") 
    
# First
class Brand(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    image = models.ImageField(blank = True)
    country = CountryField(blank = True)
    
    def get_absolute_url(self):
        return reverse_lazy("dashboard:brand_dashboard:create_brand")
    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField(default = '')
    price = models.FloatField(default=0)
    weight = models.FloatField(default = 1)
    # sku needs more work
    sku = models.UUIDField(default = uuid.uuid4, unique = True, editable = True)
    stock = models.PositiveIntegerField(default = 5)
    brand = models.ForeignKey('Brand',on_delete= models.CASCADE, null = True)
    category = models.ForeignKey('Category',on_delete= models.CASCADE, null = True)
    
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse_lazy("dashboard:product_dashboard:product_list")
    
    def get_thumbnail(self):
        return self.productimage_set.first() 

# name - image url - price - brand
    
class ProductImage(models.Model):
    # image = models.ImageField(blank = True)
    image_url = models.URLField(blank = True)
    product = models.ForeignKey('Product', on_delete = models.CASCADE)
    alt = models.CharField(max_length = 225)
    
