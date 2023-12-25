from django.urls import path
from . import views

from dashboard.decorators import user_dashboard_permission 

app_name = 'brand_dashboard'

urlpatterns = [
    path('create/', user_dashboard_permission(views.CreateBrand.as_view()), name = 'create_brand'),
    path('update/<int:pk>', user_dashboard_permission(views.UpdateView.as_view()), name = "update_brand"),
    path('list/', views.ListBrand.as_view(), name="list_brand"),
    # path('<int:pk>/', views.brand_detail, name="detail_brand"),
    path('delete/<int:pk>', user_dashboard_permission(views.delete_brand),
         name= 'delete_brand'),
]
