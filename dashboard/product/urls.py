from django.urls import path
from . import views
from dashboard.decorators import user_dashboard_permission 

app_name = 'product_dashboard'

urlpatterns = [
    path('create/', user_dashboard_permission(views.CreateProduct.as_view()),
         name= 'product_create'),
    
    path('update/<int:pk>/', user_dashboard_permission(views.UpdateProduct.as_view()),
         name= 'product_update'),
    
    path('list/', views.ListProduct.as_view(),
         name= 'product_list'),
    
    path('<int:pk>/list/images/', views.ProductImageList.as_view(),
         name= 'product_image_list'),
    
    path('<int:pk>/create/image/', user_dashboard_permission(views.create_image),
         name= 'create_image'),


    path('delete/image/<int:pk>', user_dashboard_permission(views.delete_image),
         name= 'delete_image'),
    
    path('delete/<int:pk>', user_dashboard_permission(views.delete_product),
         name= 'delete_product'),
    
    
]