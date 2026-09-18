from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
from auctions.models import *
from .models import User
from django import forms
import requests
from django.contrib.auth.decorators import login_required

class Createlisting(forms.Form):
    name = forms.CharField(
        label='Item name',
        widget=forms.TextInput(
            attrs={
            "class":"form-control",
            "id":"Name" ,
            "name":"name" ,
            "placeholder":"item name",
            }
        )
    )

    price = forms.CharField(
        label='Price',
        widget=forms.NumberInput(
            attrs={
            "class":"form-control",
            "id":"price" ,
            "name":"Price" ,
            "placeholder": "Price starts from ..",
            }
        )
    )

    description = forms.CharField(
        label="Description",
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "class":"form-control",
                "id":"price" ,
                "name":"Price" ,
                "placeholder": "add a short description ..",
            }
        )

    )



    image = forms.URLField(
        label='Image url (optional)',
        required=False,
        widget=forms.URLInput(
            attrs={
            "class":"form-control",
            "id":"image" ,
            "name":"image" ,
            "placeholder": "Plz enter a valid url",
            }
        )
    )

    

    def clean_image(self):
        image_url = self.cleaned_data["image"]
        temp_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTQloBQfR1oxndVS2Z3qfCtzcpFea_-55X9idaGUSIpAQ&s=10"
        if not image_url:
            return temp_url

        try:
            
            response = requests.get(image_url,timeout=3)

            content = response.headers.get("content-type","")
            if not content.startswith("image/"):
                
                raise forms.ValidationError("Must be a image")
        except requests.RequestException:
            return temp_url

        return image_url


    category = forms.ChoiceField(
    choices=[
        ('None','NO category'),
        ('electronics', 'Electronics'),
        ('books', 'Books'),
        ('fashion', 'Fashion'),
        ('home', 'Home & Garden'),
    ],
    initial='None',
    widget=forms.Select(attrs={
        'class':"form-select",
        
    })

)

class BidForm(forms.Form):
        # def __init__(self,*args,**kwargs):
        #     super().__init__(*args,**kwargs)

        #     self.fields['price'].label = "Current bid"
        #     self.fields['price'].widget.attrs['placeholder'] = 'Enter your bid'
        #     self.fields["price"].required = False

        #     self.fields.pop('name')
        #     self.fields.pop('description')
        #     self.fields.pop('image')

        bid = forms.CharField(
                
                widget=forms.NumberInput(
                    attrs={
                    "class":"form-control",
                    "id":"bid" ,
                    "name":"bid" ,
                    "placeholder": "Enter your bid ...",
                    }
                )
            )

def index(request):
    return render(request, "auctions/index.html",{
        "listings":Listings.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def add(request):
    if request.method == "POST":
        form = Createlisting(request.POST)
        if form.is_valid():
            
            name = form.cleaned_data["name"]
            if not (Listings.objects.filter(name=name).exists()):
                price = form.cleaned_data["price"]
                img = form.cleaned_data["image"]
                description = form.cleaned_data['description']
                category = form.cleaned_data['category']
                Listings.objects.create(name=name,price=price,image=img,description=description,category=category)
                listing = Listings.objects.last()
                Createdby.objects.create(name=request.user,listing_id=listing.id)
                return redirect('index')
            else :
                return render(request,'auctions/Add_listing.html',
                                      {
                                        'form':Createlisting(),
                                        'warning':'Listing with this name already exists'
                                        }
                                    )

        
        return render(request,'auctions/Add_listing.html',
                      {
                        'form':Createlisting(),
                        'warning':'invalid image url'
                        }
                    )
    return render(request,'auctions/Add_listing.html',{
        'form':Createlisting()
    })


def ren(request,name,data,total_bids,highest,req,id):
    warn=''
    if req == 'Higher value':
       warn = 'Bid value should be higher then current price'
    elif req == 'not_login':
       warn = 'You must first login to Bid'
    else :
     bid = False

    return render(request,'auctions/entry.html',
                                    {
                                    'data':data,
                                    'Bid':total_bids,
                                    'form':BidForm,
                                    'name':name,
                                    'id':id,
                                    'highest':highest,
                                    'warning' :warn,
                                    'created_by':Createdby.objects.get(listing_id=id),
                                    'category':data.get_category_display(),
                                })

def entry(request,name,id):
    data = Listings.objects.get(id=id)
    bid_data = Bid.objects.filter(listing_id=id) 
    total_bids = bid_data.count() 
    highest = bid_data.order_by("-amount").first()
    if request.method == 'POST':

        if request.user.is_authenticated :
            form = BidForm(request.POST)
            if form.is_valid():
                bid = form.cleaned_data['bid']

                if int(bid)<= data.price:
                    return  ren(request,name,data,total_bids,highest,'Higher value',id)
                
                Bid.objects.create(amount=bid,listing_id=id,user=request.user)
                Listings.objects.filter(id=id).update(price=bid)
                return redirect('entry',name=name,id=id)
            
            return redirect('entry',name=name,id=id)
        
        return ren(request,name,data,total_bids,highest,'not_login',id)
    
    return ren(request,name,data,total_bids,highest,0,id)