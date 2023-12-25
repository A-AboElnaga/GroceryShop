from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from .models import Checkout, CheckoutLine
from userprofile.form import ShippingAddressForm, VisitorShippingAddressForm, EditShippingAddress
from userprofile.models import UserProfile, Addresses
from django.urls import reverse
from order.models import Order, OrderLine
from .decorator import user_cookie_checkout
from product.models import Product
from .form import PaymentCardForm
from random import randint
from django.utils import timezone
from datetime import datetime, timedelta

def get_checkout(request):
    user = request.user
    if user.is_authenticated:
        return Checkout.objects.get(user=user, email=user.email)
    
    token = request.get_signed_cookie('checkout')
    return Checkout.objects.get(user=None, token=token)


def checkout_view(request):
    is_none = False
    total = 0
    try:
        checkout = get_checkout(request)
        checkout_line = checkout.checkoutline_set.all()
        for line in checkout_line:
            total += line.get_sub_total()
            
    except Checkout.DoesNotExist:
        is_none = True


    user = request.user
    if (not user.is_authenticated and request.get_signed_cookie('checkout', None) is None) or is_none:
        context = {
            'checkout_line':None
        }
        return TemplateResponse(request,'checkout/index.html', context)
    context ={
        'checkout_line': CheckoutLine.objects.filter(checkout=checkout),
        'checkout': checkout,
        'total' : round(total, 2)
    }
    return TemplateResponse(request, 'checkout/index.html', context)

@user_cookie_checkout
def create_shipping_address(request):
    checkout = get_checkout(request)
    user = request.user
    is_auth = user.is_authenticated
    if is_auth:
        form = ShippingAddressForm(request.POST or None)
    else:
        form = VisitorShippingAddressForm(request.POST or None, instance=checkout.shipping)
    context = {
        'form': form
    }
    if request.method == "POST":
        if form.is_valid():
            obj = form.save()
            if is_auth:
                profile = get_object_or_404(UserProfile, user=user)
                profile.user_addresses.add(obj)
                profile.save()
            else:
                checkout.email = request.POST.get('email')
            checkout.shipping = obj
            checkout.save()
            return HttpResponseRedirect(reverse('checkout:create_order_view'))
    else:
        if is_auth:
            addresses_form = EditShippingAddress(user=user)
            context.update({
                'addresses_form' : addresses_form,
            })
        
    return TemplateResponse(request, 'checkout/shipping_create.html', context)

@user_cookie_checkout
def edit_shipping_address(request):
    user = request.user
    
    if user.is_authenticated and request.method == "POST":
        form = EditShippingAddress(request.POST, user=user)
        if form.is_valid():
            checkout = get_checkout(request)
            checkout.shipping = Addresses.objects.get(id=int(request.POST.get('addresses')))
            checkout.save()
            return HttpResponseRedirect(reverse('checkout:create_order_view'))
    
    return HttpResponseRedirect(reverse('checkout:create_order_view'))
    
@user_cookie_checkout
def create_order_view(request):
    user = request.user
    checkout = get_checkout(request)
    checkout_line = checkout.checkoutline_set.all()
    total = 0

    if checkout_line.count() > 0:
        for line in checkout_line: 
            total += line.get_sub_total()
    total = round(total, 2)
    if request.method == "POST":
        if checkout_line.count() > 0:
            form = PaymentCardForm(request.POST)
            
            if not form.is_valid():
                context = {
                    'checkout_line': checkout_line,
                    'checkout': checkout,
                    'total': total,
                    'form': form
                }
                return TemplateResponse(request, 'checkout/confirm_order.html', context)
            
            if user.is_authenticated:
                order = Order.objects.create(checkout_token=checkout.token, user=user, 
                                             email=user.email, shipping=checkout.shipping, total=total)
                
            else:
                order = Order.objects.create(checkout_token=checkout.token, email=checkout.email, 
                                               shipping=checkout.shipping, total=total)
            
            # print("-"*20)

            for line in checkout_line:
                product = line.product
                order_line = OrderLine.objects.create(order=order, product=product, 
                                        product_name=product.name, product_price=product.price, 
                                        sku=product.sku, quantity=line.quantity)
                
                # total += order_line.get_sub_total()
                Product.objects.filter(sku=product.sku).update(stock=product.stock-line.quantity)
                # real_product.
            
            order.total = total
            order.save()
            checkout.delete()
            response = HttpResponseRedirect(reverse('order:detail_order', kwargs={
                'pk': order.pk,    
            }))
            response.delete_cookie('checkout', None)
            return response
    
    form = PaymentCardForm()
    
    context = {
        'checkout_line': checkout_line,
        'checkout': checkout,
        'total': total,
        'form': form
    }
    return TemplateResponse(request, 'checkout/confirm_order.html', context)


def delete_item(request,pk):
    item = get_object_or_404(CheckoutLine,pk=pk) 
    if item:
        item.delete()
        return checkout_view(request)
        # return JsonResponse({'message' : 'the item has been deleted successfully from cart'},status=200)
    
    return JsonResponse({'message':'this item is not your card'}, status=400)