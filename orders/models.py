from django.db import models
from restaurants.models import Restaurant  
from users.models import User
# Create your models here.
class Orders(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateTimeField()

    def __str__(self):
        return self.user, self.restaurant, self.total, self.start_date
    
    def to_dict(self):
        return {
            'user': self.user.id,
            'restaurants': self.restaurants.id,
            'total': self.total,
            'start_date': self.start_date
        }
