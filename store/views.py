from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
import json
from .models import *
import datetime
from .utils import cartData, cookieCart, guestOrder

# Create your views here.
def home(request):
    products = Product.objects.all()[:6]
    context = {"products": products}
    return render(request, "store/home.html", context)

def product_detail(request, pk):
    # return HttpResponse("This is the detials page")
    data = cartData(request)
    cart_items = data["cart_items"]
    product = get_object_or_404(Product, pk=pk)
    context = {"product": product, "cart_items": cart_items}
    return render(request, "store/product_detail.html", context)

def store(request):
    data = cartData(request)
    cart_items = data["cart_items"]
 
    products = Product.objects.all()
    context = {"products": products, "cart_items": cart_items}
    return render(request, "store/store.html", context)

def cart(request):
    data = cartData(request)
    items = data["items"]
    order = data["order"]
    cart_items = data["cart_items"]
    context = {"items": items, "order": order, "cart_items": cart_items}
    return render(request, "store/cart.html", context)

def main(request):
    context = {}
    return render(request, "store/main.html", context)

def checkout(request):
    data = cartData(request)
    items = data["items"]
    order = data["order"]
    cart_items = data["cart_items"]
    context = {"items": items, "order": order, "cart_items": cart_items}
    return render(request, "store/checkout.html", context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data["productId"]
    action = data["action"]
    # print("Action: " + action)
    # print("productId: " + productId)
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, completed=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    print(created)
    if action == "add":
        orderItem.quantity = orderItem.quantity + 1
    elif action == "remove":
        orderItem.quantity = orderItem.quantity - 1
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse("item was added", safe=False)

def processOrder(request):
    # print(json.loads(request.body))
    data = json.loads(request.body)
    transaction_id = datetime.datetime.now().timestamp()

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        
        if order.shipping == True:
            ShippingAddress.objects.create(
                customer = customer,
                order = order,
                address = data["shipping"]["address"],
                city = data["shipping"]["city"],
                state = data["shipping"]["state"],
                zipcode = data["shipping"]["zipcode"],
            )
    else:
        customer, order = guestOrder(request, data)

    total = float(data["form"]["total"])
    order.transaction_id = transaction_id
    # print(total == order.get_total_items())
    if total == order.get_total_items:
        order.completed = True
    order.save()
    if order.shipping == True:
        ShippingAddress.objects.create(
            customer = customer,
            order = order,
            address = data["shipping"]["address"],
            city = data["shipping"]["city"],
            state = data["shipping"]["state"],
            zipcode = data["shipping"]["zipcode"],
        )

    return JsonResponse("Payment complete", safe=False)