# store/models/viewlog.py
from django.db import models
from store.models.customer import Customer
from store.models.product import Products

class ProductView(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer} viewed {self.product.name} at {self.timestamp}"
