#This whole file is new

from django.shortcuts import render
from order.models import Order, OrderLine
from django.template.response import TemplateResponse

def index(request):

    user = request.user
    orders = []
    if user.is_authenticated:
        orders = Order.objects.filter(user=user).all()

    
    # return render("dashboard/index.html", {
    #     "orders": orders,
    # })
    context = {"orders": orders}
    return TemplateResponse(request,'dashboard/index.html', context)
