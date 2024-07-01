from django.db import models

from apps.core.models import Model


class ShippingMethod(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    estimated_delivery_time = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name


class ShippingAddress(models.Model):
    # order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name="shipping_addresses")
    name = models.CharField(max_length=255)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=255)
    country = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} - {self.address_line_1}"


class Shipment(Model):
    # order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name="shipments")
    shipping_method = models.ForeignKey('ShippingMethod', on_delete=models.SET_NULL, null=True)
    tracking_number = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
        # return f"Shipment for order {self.order.id}"
