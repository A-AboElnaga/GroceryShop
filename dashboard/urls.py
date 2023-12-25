from django.urls import path, include
from .category import urls as category_url
from .product import urls as product_url
from .brand import urls as brand_url
from .views import index
app_name = "dashboard"

urlpatterns = [
    path('index/', index, name="index"),
    path('category/', include(category_url, namespace = 'category_dashboard')),
    path('product/', include(product_url, namespace = 'product_dashboard')),
    path('brand/', include(brand_url, namespace = 'brand_dashboard')),
    
]

