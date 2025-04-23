from django.db import models
from restaurants.models import Restaurant  
from users.models import User


# Create your models here.
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=2, decimal_places=1)
    comment = models.TextField()
    start_date = models.DateTimeField()

    def __str__(self):
        return self.user, self.restaurant, self.score, self.comment, self.start_date
    

    def to_dict(self):
        return {
            'user': self.user.id,
            'restaurant': self.restaurant.id,
            'score': self.score,
            'comment': self.comment,
            'start_date': self.start_date
        }