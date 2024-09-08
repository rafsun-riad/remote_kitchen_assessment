from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


# Create your models here.


class User(AbstractUser):  # extended user model for permission
    is_owner = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)


# auto generate token for registered user
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Restaurant(models.Model):  # restuarant model with owner
    owner = models.ForeignKey(
        # used settings.AUTH_USER_MODEL because changed the django user model
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='restaurant')

    name = models.CharField(max_length=200)
    location = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Employee(models.Model):  # employee model
    employee = models.ForeignKey(
        # used settings.AUTH_USER_MODEL because changed the django user model
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='employee')

    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.SET_NULL, null=True, related_name='employee')


class Category(models.Model):  # category model
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name='category')

    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Menu(models.Model):  # menu model
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='menu')

    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class FoodItem(models.Model):  # fooditem model
    menu = models.ForeignKey(
        Menu, on_delete=models.CASCADE, related_name='fooditem')

    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return f'{self.name} | {self.price}'


class Modifier(models.Model):  # fooditem modifier
    food_item = models.ForeignKey(
        FoodItem, on_delete=models.SET_NULL, null=True, blank=True, related_name='modifier')
    name = models.CharField(max_length=200)
    extra_price = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)


class Order(models.Model):  # order model
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='order')

    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name='order', null=True, blank=True)

    total_price = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)

    ordered_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    is_paid = models.BooleanField(default=False)

    payment_method = models.CharField(max_length=150, null=True, blank=True)

    paid_at = models.DateTimeField(
        auto_now_add=False, null=True, blank=True)

    delivery_address = models.CharField(max_length=300, null=True, blank=True)


class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,
                              null=True, blank=True, related_name='order_items')

    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name='order', null=True, blank=True)

    menu = models.ForeignKey(
        Menu, on_delete=models.SET_NULL, related_name='order', null=True, blank=True)

    food_item = models.ForeignKey(
        FoodItem, on_delete=models.SET_NULL, null=True, blank=True, related_name='order')
