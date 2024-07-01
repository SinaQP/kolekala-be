from django.db import models
from apps.core.models import Model


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
