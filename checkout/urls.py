from django.urls import path
from .views import checkout_view,create_shipping_address, edit_shipping_address, create_order_view
from .views import delete_item
from dashboard.decorators import user_dashboard_permission 

app_name = "checkout"
urlpatterns = [
    path('',checkout_view, name="checkout_index"),
    path('create/address/', create_shipping_address, name="checkout_create_address"),
    path('edit/address/', edit_shipping_address, name="checkout_edit_address"),
    path('create/order/', create_order_view, name="create_order_view"),
    path('delete/<int:pk>', delete_item, name= 'delete_item'),    
]
