from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ...



class Listing(models.Model):
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
    highest_bidder = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name='highest')
    
    def __str__(self):
        return f'{self.name}'



class Bid(models.Model):

    user = models.ForeignKey(User,on_delete=models.SET_NULL,related_name='bid',null=True)
    listing = models.ForeignKey(Listing,on_delete=models.CASCADE,related_name='bid')
    amount = models.IntegerField()
    def __str__(self):
        return f'{self.amount}'


class Createdby(models.Model):
     listing = models.OneToOneField(Listing,on_delete=models.CASCADE,related_name="created_by",unique=True)
     name = models.ForeignKey(User,on_delete=models.SET_NULL,related_name='created',null=True)

     def __str__(self):
         return f'{self.name}'


class Sold(models.Model):
    listing = models.OneToOneField(Listing,on_delete=models.CASCADE,related_name='sold')
    status =  models.BooleanField(default=True)
    sold_at = models.DateTimeField(auto_now=True)
    sold_to = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True,related_name='sold' )
 
    def __str__(self):
        return f'{self.sold_to}'


class Comment(models.Model):
    listing = models.ForeignKey(Listing,on_delete=models.CASCADE,related_name='comment')
    comment = models.CharField(max_length=100)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='comment')
    
    def __str__(self):
        return f'{self.comment}'


class Wishlist(models.Model):
    listing = models.OneToOneField(Listing,on_delete=models.CASCADE,related_name='wishlist',null=True)
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return f'{self.listing}'