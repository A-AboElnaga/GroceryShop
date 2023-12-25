from typing import Any
from django.db.models.query import QuerySet
from django.http import JsonResponse
from django.utils.text import slugify
from django.views.generic import CreateView, UpdateView, ListView
from product.models import Product,ProductImage, Category
from order.models import OrderLine
from django.shortcuts import get_object_or_404, render
from .forms import ProductImageForm
from django.urls import reverse
from .forms import FilterForm
from django.db.models import Count
from math import inf


class CreateProduct(CreateView):
    model = Product
    template_name = "dashboard/product/create.html"
    fields = ["name", 'description', 'price', 'weight', 'sku', 
              'stock', 'brand', 'category']
    
    def form_valid(self, form):
        instance = form.save()
        instance.slug = slugify(instance.name) + "-" + str(instance.id)
        instance.save()
        
        return super(CreateProduct, self).form_valid(form)
    

class UpdateProduct(UpdateView):
    model = Product
    template_name = "dashboard/product/create.html"
    fields = ["name", 'description', 'price', 'weight', 'sku', 
              'stock', 'brand', 'category']

    
    def form_valid(self, form):
        instance = form.instance
        instance.slug = slugify(instance.name) + "-" + str(instance.id)
        instance.save()
        
        return super(UpdateProduct, self).form_valid(form)
    
class ListProduct(ListView):
    model = Product
    template_name = "dashboard/product/list.html"
    paginate_by = 12
    context_object_name = "product_list"

    def get_queryset(self):
        queryset = super().get_queryset()


        # Filter queryset based on price if form data is present
        best_sellers = self.request.GET.get('submit_action') == 'best_sellers'
        
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        if (min_price != '' and min_price is not None) or (max_price != '' and max_price is not None):
            
            if min_price == '' or min_price is None:
                min_price = 0
            
            if max_price == '' or max_price is None:
                max_price = inf
        
            queryset = queryset.filter(price__gte=min_price, price__lte=max_price)
            
        
        # based on brand nationality
        brand_Nationality = self.request.GET.get('brand_Nationality')
        if brand_Nationality != '' and brand_Nationality is not None:
            queryset = queryset.filter(brand__country__iexact = brand_Nationality)
        
        
        # based on brand name
        brand_name = (self.request.GET.get('brand_name'))            
        if brand_name != '' and brand_name is not None:
            brand_name = brand_name.lower()
            queryset = queryset.filter(brand__name__icontains = brand_name)
        
        
        # based on brand name choice
        brand_name_choice = (self.request.GET.get('brand_name_choice'))
        if brand_name_choice != '' and brand_name_choice is not None:
            brand_name_choice = brand_name_choice.lower()            
            queryset = queryset.filter(brand__name__iexact = brand_name_choice)
        
        
        # based on product name
        product_name = (self.request.GET.get('product_name'))            
        if product_name != '' and product_name is not None:
            product_name = product_name.lower()
            queryset = queryset.filter(name__icontains = product_name)
        
        if best_sellers:
            queryset = queryset.annotate(orders_count = Count('orderlines'))
            queryset = queryset.order_by("-orders_count", "name")
        else:
            queryset = queryset.order_by("name")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Pass the form to the template
        context['filter_form'] = FilterForm(self.request.GET)

        return context
    
    
    
class ProductImageList(ListView):
    model = ProductImage
    template_name = 'dashboard/product/list_images.html'    
    

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductImageList, self).get_context_data(**kwargs)
        context['form'] = ProductImageForm()
        context['product_id'] = self.kwargs.get('pk')
        return context
    
    def get_queryset(self):
        return super(ProductImageList, self).get_queryset().filter(product__id=self.kwargs.get('pk'))
    
def create_image(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = ProductImageForm(request.POST, request.FILES)
    if form.is_valid():
        obj = form.save(commit = False)
        obj.product = product
        obj.alt = product.name
        obj.save()
        return JsonResponse({
            'message':'product image successfully created','alt' : obj.alt,
            'url': obj.image.url,
            'delete_url': reverse('dashboard:product_dashboard:delete_image',kwargs={
                                 'pk': obj.pk})}, 
            status = 200)
    
    return JsonResponse({'message':form.errors}, status = 400)

def delete_image(request,pk):
    product_image = get_object_or_404(ProductImage,pk=pk) 
    if product_image:
        product_image.delete()
        return JsonResponse({'message' : 'the image has been deleted successfully'},status=200)
    
    return JsonResponse({'message':'this product image instance does not exist'}, status=400)

def delete_product(request,pk):
    product = get_object_or_404(Product,pk=pk) 
    if product:
        product.delete()
        return JsonResponse({'message' : 'the product has been deleted successfully'},status=200)
    
    return JsonResponse({'message':'this product instance does not exist'}, status=400)