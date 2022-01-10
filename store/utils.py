import json
from .models import *

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES["cart"])
    except:
        cart = {}
    items = []
    order = {"get_total_items": 0, "get_total_price": 0, "shipping": False}
    cart_items = order.get("get_total_items")
    for i in cart:
        try:
            cart_items += cart[i]["quantity"]
            product = Product.objects.get(id=i)
            total = (product.price * cart[i]["quantity"])
            order["get_total_price"] += total
            order["get_total_items"] += cart[i]["quantity"]
            item = {
                "product": {
                    "id": product.id,
                    "name": product.name,
                    "price": product.price,
                    "image": product.image
                },
                "quantity": cart[i]["quantity"],
                "get_total": total
            }
            items.append(item)
            if product.digital == False:
                order["shipping"] = True
        except:
            pass
    return {"cart_items": cart_items, "order": order, "items": items}

def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        items = order.order_items.all()
        cart_items = order.get_total_items
    else:
        cookieData = cookieCart(request)
        items = cookieData["items"]
        order = cookieData["order"]
        cart_items = cookieData["cart_items"]
    return {"cart_items": cart_items, "order": order, "items": items}

def guestOrder(request, data):
    print("User is not logged in")
    print(json.loads(request.body))
    name = data["form"]["name"]
    email = data["form"]["email"]
    cookieData = cookieCart(request)
    items = cookieData["items"]

    customer, created = Customer.objects.get_or_create(email=email)
    customer.name = name
    customer.save()

    order = Order.objects.create(customer=customer, completed=False)
    for item in items:
        product = Product.objects.get(id=item["product"]["id"])
        orderItem = OrderItem.objects.create(product=product, order=order, quantity=item["quantity"])

    return customer, order