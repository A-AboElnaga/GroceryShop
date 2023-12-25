from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404,render
from django.views.generic import ListView, DetailView
from .models import Product, Category, Brand
from order.models import Order, OrderLine
from checkout.form import CheckoutLineForm
from checkout.models import CheckoutLine, Checkout
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import timedelta
from django.utils import timezone


def detail_product(request, slug, form = None):
    product = get_object_or_404(Product, slug=slug)
    if not form:
        form = CheckoutLineForm(request.POST or None, product = product)
    total_users = OrderLine.objects.filter(product=product)
    
    twenty_four_hours_ago = timezone.now() - timedelta(days = 1)
    users_last_24 = total_users.filter(order__created__gte=twenty_four_hours_ago)
    context = {
        'form':form,
        'object':product,
        'users_total': total_users.count(), #
        'users_last_24': users_last_24.count() #
    }
    return render(request,'product/detail.html', context)
        

class ListProduct(ListView):
    model = Product
    template_name = 'product/list.html'  
    paginate_by = 12
    
    def get_queryset(self):
        category = get_object_or_404(Category, slug = self.kwargs.get('slug'))
        categories = category.get_descendants(include_self=True)
        qs = super(ListProduct,self).get_queryset().filter(
            category__in=categories
        ).order_by('name')
        
        return qs
class ListProductBrand(ListView):
    model = Product
    template_name = 'product/list.html'  
    paginate_by = 12
    
    def get_queryset(self):
        brand = get_object_or_404(Brand, slug = self.kwargs.get('slug'))
        qs = super(ListProductBrand,self).get_queryset().filter(
            brand__exact= brand
        ).order_by('name')
        
        return qs
    
def get_or_create_checkout(request, checkout_queryset = Checkout.objects.all()):
    user = request.user
    if user.is_authenticated:
        
        return checkout_queryset.get_or_create(
            user = user,
            email = user.email
        )[0]
        
    token = request.get_signed_cookie('checkout', default = None)
    return checkout_queryset.filter(token = token, user = None).get_or_create(
        user = None
    )[0]
        
 
def set_checkout_cookie(checkout,response):
    max_age = int(timedelta(days=30).total_seconds())
    response.set_signed_cookie('checkout', checkout.token, max_age=max_age)
    
    
def add_product_to_checkout(request, pk):
    product = get_object_or_404(Product, pk = pk)
    if request.method == "POST":
        checkout = get_or_create_checkout(request)
        instance = CheckoutLine(product=product, checkout=checkout)
        form = CheckoutLineForm(request.POST, instance=instance, product=product)
        
        if form.is_valid():
            checkout_line = CheckoutLine.objects.filter(
                product=product,
                checkout=checkout
            )
            if checkout_line.exists():
                instance = checkout_line[0]
                instance.quantity += int(request.POST.get('quantity'))
                instance.save()
            
            else:            
                form.save()                 
            
            # Changed Here   
            response = HttpResponseRedirect(reverse('checkout:checkout_index'))
            
        else:
            response = detail_product(request,product.slug,form)
            
        if not request.user.is_authenticated:
            set_checkout_cookie(checkout, response)
            
        return response
    return HttpResponseRedirect(reverse('checkout:checkout_index'))
