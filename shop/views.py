from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
import json

from django.db.models import Sum
from .models import *

def products(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']  # which is zero here

    products = Product.objects.all()
    context = { 
        'products': products,
        'cartItems': cartItems
    }
    return render(request, 'products.html', context)  # load the item_list as context

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)  # Retrieve the item based on ID
    context = { 
        'product': product 
    }
    return render(request, 'product_detail.html', context)  # Render the item detail template

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, }
    
    context = { 
        'items': items 
    }
    return render(request, 'cart.html', context)

def update_item(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    
    print('product id', productId)
    print('action', action)

    customer = request.user.customer
    product = Product.objects.get(id=productId)

    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1) 
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, }
    
    context = { 
        'items': items 
    }
    return render(request, 'checkout.html', context)

def main(request):
    return render(request, 'main.html')

