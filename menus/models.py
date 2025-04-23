from django.db import models
from restaurants.models import Restaurant  

# Create your models here.
class Menu(models.Model):
    restaurants = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="menus")
    name = models.CharField(max_length=256)
    description = models.TextField()
    start_date = models.DateTimeField()

    def __str__(self):
        return self.name, self.description, self.start_date, self.restaurants

    def to_dict(self):
        return {
            'restaurants': self.restaurants.id,
            'name': self.name,
            'description': self.description,
            'start_date': self.start_date
        }