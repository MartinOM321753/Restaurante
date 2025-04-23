from django.db import models

# Create your models here.

class Role(models.Model):
    name = models.CharField(max_length=16, unique=True)
    
    def __str__(self):
        return self.name
    
    def to_dict(self):
        return {
            'name':self.name
        }