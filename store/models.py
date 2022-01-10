from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE, related_name="customer")
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    digital = models.BooleanField(default=False, null=True, blank=True)
    image = models.ImageField(default="placeholder.png", blank=True)
    description= models.TextField(null=True, blank=True)
    additional_info = models.TextField(null=True, blank=True)
    sub_image1 = models.ImageField(null=True, blank=True)
    sub_image2 = models.ImageField(null=True, blank=True)
    sub_image3 = models.ImageField(null=True, blank=True)


    def __str__(self):
        return self.name

    @property
    def other_images(self):
        if(self.sub_image1 or self.sub_image2 or self.sub_image3):
            return True
        else: 
            return False

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, related_name="orders")
    date_ordered = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False, blank=True, null=True)
    transaction_id = models.CharField(max_length=200, null=True)

    @property
    def get_total_items(self):
        order_items = self.order_items.all()
        total = sum([item.quantity for item in order_items])
        return total

    @property
    def get_total_price(self):
        order_items = self.order_items.all()
        total = sum([item.get_total for item in order_items])
        return total

    @property
    def shipping(self):
        order_items = self.order_items.all()
        shipping = False
        for item in order_items:
            if item.product.digital == False:
                shipping = True
        return shipping

    def __str__(self):
        return str(self.id)

class OrderItem(models.Model):
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL, related_name="order_items")
    order = models.ForeignKey(Order, null=True, on_delete=models.SET_NULL, related_name="order_items")
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return self.product.name

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL, related_name="address")
    order = models.ForeignKey(Order, null=True, on_delete=models.SET_NULL, related_name="address")
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)