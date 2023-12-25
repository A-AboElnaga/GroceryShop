from django.urls import path
from . import views
from dashboard.decorators import user_dashboard_permission 

app_name = 'category_dashboard'

urlpatterns = [
    path('create/', user_dashboard_permission(views.CreateCategory.as_view()), name = "category_create"),
    path('create/<int:pk>/', user_dashboard_permission(views.CreateSubCategory.as_view()), name = "sub_category_create"),
    path('update/<int:pk>/', views.UpdateCategory.as_view(), name = "category_update"),
    path('list/', views.CategoryList.as_view(), name = "category_list"),
    path('<int:pk>/', views.category_detail, name = "category_detail"),
    
    path('delete/<int:pk>', user_dashboard_permission(views.delete_category),
         name= 'delete_category'),
    
]

 