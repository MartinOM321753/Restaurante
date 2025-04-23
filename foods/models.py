from django.db import models
from menus.models import Menu

class Foods(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="foods")
    name = models.CharField(max_length=256)
    stock = models.IntegerField(null=False)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            'menu': self.menu.id,
            'name': self.name,
            'description': self.description,
            'price': float(self.price),
            'start_date': self.start_date.isoformat()
        }
