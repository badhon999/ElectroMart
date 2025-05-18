from django.db import models
from store.models.customer import Customer

class SearchHistory(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    query = models.CharField(max_length=255)
    searched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.email} - {self.query}"
