from django.urls import path
from .views import DetailOrder, ListOrder

app_name = 'order'
urlpatterns = [
    path('<int:pk>/', DetailOrder.as_view(), name="detail_order"),
    path('', ListOrder.as_view(), name="list_order"),
]
