from django.db import models
from foods.models import Foods
# Create your models here.

class FoodImage(models.Model):
    food = models.OneToOneField(Foods,related_name='image',on_delete=models.CASCADE,null=False)
    data = models.BinaryField(null=False)
    name = models.CharField(max_length=200, null=False)
    type = models.CharField(max_length=100,null=False)