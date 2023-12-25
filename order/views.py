from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from .models import Order, OrderLine
from django.views.generic import DetailView, ListView

# Create your views here.
class DetailOrder(DetailView):
    paginate_by = 12
    model = Order
    template_name = 'order/detail.html'
    
    
class ListOrder(ListView):
    model = Order
    template_name = 'order/list.html'
    paginate_by = 12
    
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return super(ListOrder, self).get_queryset().filter(user=user, email=user.email)