from django.db import models
from restaurants.models import Restaurant  # o como se llame tu modelo de restaurante
from users.models import User
class Sale(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Venta #{self.id} - Restaurante {self.restaurant.name}"
