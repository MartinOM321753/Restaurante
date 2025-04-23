from django.db import models
from restaurants.models import Restaurant
# Create your models here.

class Restaurant_image(models.Model):
    restaurant = models.OneToOneField(Restaurant,related_name='restaurant_image',on_delete=models.CASCADE,null=False)
    data = models.BinaryField(null=False)
    name = models.CharField(max_length=200,null=False)
    type = models.CharField(max_length=100,null=False)