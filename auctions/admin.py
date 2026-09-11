from django.contrib import admin
from auctions.models import *
# Register your models here.

class AdminListing(admin.ModelAdmin):
    list_display = ("id","name","price","created_on","image")


admin.site.register(Listings,AdminListing)