from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ...



class Listings(models.Model):
    name = models.CharField(max_length=60)
    price = models.IntegerField()
    image = models.URLField(max_length=300,blank=True,null=True)
    created_on = models.DateTimeField(auto_created=True,auto_now_add=True)
    description  = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}{self.price}{self.image}{self.created_on}'



class Bid(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='bid')
    listing = models.ForeignKey(Listings,on_delete=models.CASCADE,related_name='bid')
    amount = models.IntegerField()
    def __str__(self):
        return f'{self.amount}'