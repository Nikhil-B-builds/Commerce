from django.contrib import admin
from auctions.models import *
# Register your models here.

class AdminListing(admin.ModelAdmin):
    list_display = ("id","name","price","created_on","image",'Categories')
    

class Userlisting(admin.ModelAdmin):
    list_display = ('id','last_login','username','email','is_superuser','date_joined')

class bidlisitng(admin.ModelAdmin):
    list_display =('id','amount','user_id','listing_id')

class createdlisting(admin.ModelAdmin):
    list_display = ('id','listing_id','name')

admin.site.register(Listings,AdminListing)
admin.site.register(User,Userlisting)
admin.site.register(Createdby,createdlisting)
admin.site.register(Bid,bidlisitng)