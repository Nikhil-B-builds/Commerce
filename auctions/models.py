from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ...



class Listings(models.Model):
    name = models.CharField(max_length=60,unique=True)
    price = models.IntegerField()
    image = models.URLField(max_length=300,default='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTQloBQfR1oxndVS2Z3qfCtzcpFea_-55X9idaGUSIpAQ&s=10')
    created_on = models.DateTimeField(auto_created=True,auto_now_add=True)
    description  = models.CharField(max_length=100)
    category = models.CharField(
        max_length=20,
        choices=[ 
        ('None','No_category'),
        ('electronics', 'Electronics'),
        ('books', 'Books'),
        ('fashion', 'Fashion'),]
    )
    def __str__(self):
        return f'{self.name}{self.price}{self.image}{self.created_on}'



class Bid(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='bid')
    listing = models.ForeignKey(Listings,on_delete=models.CASCADE,related_name='bid')
    amount = models.IntegerField()
    def __str__(self):
        return f'{self.amount}'


class Createdby(models.Model):
     listing = models.ForeignKey(Listings,on_delete=models.CASCADE,related_name="created_by",unique=True)
     name = models.CharField(default=User,max_length=60)

     def __str__(self):
         return f'{self.name}'

