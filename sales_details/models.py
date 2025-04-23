from django.db import models
from foods.models import Foods
from sales.models import Sale

class SaleDetail(models.Model):
    sale = models.ForeignKey(Sale, related_name='details', on_delete=models.CASCADE)
    food = models.ForeignKey(Foods, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.unit_price = self.food.price
        self.subtotal = self.quantity * self.unit_price
        super().save(*args, **kwargs)
