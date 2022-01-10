from django.urls import path
from . import views

app_name = "store"

urlpatterns = [
    path("", views.home, name="home"),
    path("store", views.store, name="store"),
    path("store/products/<int:pk>", views.product_detail, name="product_detail"),
    path("cart", views.cart, name="cart"),
    path("checkout", views.checkout, name="checkout"),
    path("update_item", views.updateItem, name="update_item"),
    path("process_order", views.processOrder, name="process_order")
]