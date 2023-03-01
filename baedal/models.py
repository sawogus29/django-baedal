from django.db import models

# Create your models here.
class Restaurant(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    display_name = models.CharField(max_length=50)
    category = models.CharField(choices=models.TextChoices('Category', 'Chicken Pizza Chinese Korean').choices, max_length=50)

class Customer(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    
class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    price = models.IntegerField()

class Purchase(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.SET_NULL, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    total_price = models.IntegerField()
    status = models.CharField(choices=models.TextChoices('StatusType', 'Pending Accepted Rejected').choices, max_length=50)
    created_date = models.DateTimeField()

class PurchaseMenu(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    quantity = models.IntegerField()
