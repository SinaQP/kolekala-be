from django.db import models

from apps.accounts.models import User
from apps.core.models import Model


class Shop(Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shops')
    description = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=500)
    city = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    website = models.URLField(blank=True, null=True)
    logo = models.ImageField(upload_to='shop_logos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Product(Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True)
    inventory = models.PositiveIntegerField(default=0)
    category = models.ForeignKey('ProductCategory', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class ProductCategory(Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    parent_category = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, related_name='child_categories')

    def __str__(self):
        return self.name
