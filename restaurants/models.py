from django.db import models
from users.models import User


class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.TextField()
    logo = models.TextField()
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)


    def __str__(self):
        return self.name, self.address, self.phone, self.logo, self.description, self.user, self.start_date
    
    def to_dict(self):
        return {
            'name':self.name,
            'address':self.address,
            'phone':self.phone,
            'logo':self.logo,
            'description':self.description,
            'user':self.user,
            'start_date': self.start_date
        }