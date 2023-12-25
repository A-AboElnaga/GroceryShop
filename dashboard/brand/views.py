from django.utils.text import slugify
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from product.models import Brand, Product
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse

class CreateBrand(CreateView):
    model = Brand
    template_name = "dashboard/brand/create.html"
    fields = ["name", 'image']
    
    def form_valid(self, form):
        instance = form.save()
        instance.slug = slugify(instance.name) + "-" + str(instance.id)
        instance.save()
        
        return super(CreateBrand, self).form_valid(form)
    

class UpdateBrand(UpdateView):
    model = Brand
    template_name = "dashboard/brand/create.html"
    fields = ["name", 'image']
    
    def form_valid(self, form):
        instance = form.instance
        instance.slug = slugify(instance.name) + "-" + str(instance.id)
        instance.save()
        
        return super(UpdateBrand, self).form_valid(form)
    
class ListBrand(ListView):
    model = Brand
    template_name = "dashboard/brand/list.html"
    paginate_by = 12
    def get_queryset(self):
        return super().get_queryset().order_by('name')
    
    
# class DetailBrand(DetailView):
#     model = Brand
#     template_name = "dashboard/brand/detail.html"


# def brand_detail(request, pk):

#     brand = get_object_or_404(Brand, pk = pk)
#     products = Product.objects.filter(brand = brand)
#     context = {
#         'brand' : brand,
#         'products' : products,
#     }
    
#     return render(request, 'dashboard/brand/detail.html', context)
    

def delete_brand(request,pk):
    brand = get_object_or_404(Brand,pk=pk) 
    if brand:
        brand.delete()
        return JsonResponse({'message' : 'the brand has been deleted successfully'},status=200)
    
    return JsonResponse({'message':'this brand instance does not exist'}, status=400)