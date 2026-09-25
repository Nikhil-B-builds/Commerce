from django.contrib import admin
from auctions.models import *
# Register your models here.

class AdminListing(admin.ModelAdmin):
    list_display = ("id","name","highest_bidder","price","created_on","image","category")
    

class Userlisting(admin.ModelAdmin):
    list_display = ('id','last_login','username','email','is_superuser','date_joined')

class bidlisitng(admin.ModelAdmin):
    list_display =('id','amount','user_id','listing_id')

class createdlisting(admin.ModelAdmin):
    list_display = ('id','listing_id','name_id')

class Soldadmin(admin.ModelAdmin):
    list_display= ( 'id','sold_to_id','sold_at','listing_id','status')

class Commentadmin(admin.ModelAdmin):
    list_display = ('id',"comment",'listing_id','user_id',)
    
admin.site.register(Sold,Soldadmin)
admin.site.register(Listing,AdminListing)
admin.site.register(User,Userlisting)
admin.site.register(Createdby,createdlisting)
admin.site.register(Bid,bidlisitng)
admin.site.register(Comment,Commentadmin)