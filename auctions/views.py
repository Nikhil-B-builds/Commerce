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
from django.contrib import messages

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


class Commentform(forms.Form):
    comment = forms.CharField(
        label='Add a Comment',
        max_length=100,
        widget=forms.TextInput(attrs={
        'class':'form-control',
        'id':'comment_text',
        'placeholder':'Type here ...'
        })
    )

def index(request):
   
    
    return render(request, "auctions/index.html",{
        "listings":Listing.objects.all(),
        
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
            if not (Listing.objects.filter(name=name).exists()):
                price = form.cleaned_data["price"]
                img = form.cleaned_data["image"]
                description = form.cleaned_data['description']
                category = form.cleaned_data['category']
                Listing.objects.create(name=name,price=price,image=img,description=description,category=category,highest_bidder=request.user)
                
                listing = Listing.objects.order_by("-id").first()
                Createdby.objects.create(name=request.user,listing_id=listing.id)

               
                Sold.objects.create(listing_id=listing.id,)
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
    warn= req or False
    

    return render(request,'auctions/entry.html',
                                    {
                                    'data':data,
                                    'Bid':total_bids,
                                    'bidform':BidForm,
                                    'name':name,
                                    'id':id,
                                    'highest':highest,
                                    'warning' :warn,
                                    'created_by':Createdby.objects.get(listing_id=id),
                                    'category':data.get_category_display(),
                                    'listing':Listing,
                                    'comments':Comment.objects.filter(listing_id=id),
                                    'comform':Commentform,
                                    'wishlist':Wishlist.objects.filter(listing_id=id,user=request.user) 
                                })


def bid(request,name,data,total_bids,highest,id):
    if request.user.is_authenticated :
        
        form = BidForm(request.POST)
        if form.is_valid():
            bid = form.cleaned_data['bid']
            if int(bid)<= data.price:
                return  ren(request,name,data,total_bids,highest,'Higher value',id)
                     
            Bid.objects.create(amount=bid,listing_id=id,user=request.user)
            Listing.objects.filter(id=id).update(price=bid,highest_bidder=request.user)
            return redirect('entry',name=name,id=id)
                 
        return redirect('entry',name=name,id=id)
    messages.warning(request, "You need to log in to bid.")
    return redirect('login')

def entry(request,name,id):
    data = Listing.objects.get(id=id)
    bid_data = Bid.objects.filter(listing_id=id)
    total_bids = bid_data.count() 
    highest = bid_data.order_by("-amount").first()
    if request.method == 'POST':
         return bid(request,name,data,total_bids,highest,id)
    return ren(request,name,data,total_bids,highest,0,id)

@login_required
def close(request,name,id):
    if request.method == 'POST':
        data = Sold.objects.get(listing_id=id)
        data.status = False
        data.sold_to = Listing.objects.get(id=id).highest_bidder
        data.save()
        return redirect('index')
    return redirect('entry',name=name,id=id)

def comment(request,name,id):
    if request.user.is_authenticated:

        if request.method == 'POST':
            form = Commentform(request.POST)
            if form.is_valid():
                comment = form.cleaned_data['comment']
                Comment.objects.create(user=request.user,listing_id=id,comment=comment)
                return redirect('entry',name=name,id=id)
            return redirect('entry',name=name,id=id)
        return redirect('entry',name=name,id=id)
    messages.warning(request, "You need to log in to comment.")
    return redirect('login')


def wishlist(request,name):
   if request.user.is_authenticated:
        return render(request,'auctions/wishlist.html',{
                        'data':Wishlist.objects.filter(user=request.user)
                    }
        )
   messages.warning(request, "You need to log in to see your wishlist.")
   return redirect('login')

def wishlist_add(request,name,id):
    
    if request.user.is_authenticated:
            Add_in = lambda request,id: Wishlist.objects.create(user=request.user,listing_id=id)
            back = lambda id : redirect('entry',name=Listing.objects.get(id=id).name,id=id)
                
            if request.method == 'POST':
                Add_in(request,id)
            
            if Wishlist.objects.filter(listing_id=id,user=request.user) and request.method != 'POST':
               Add_in(request,id)
               
            return back(id)

        
        
    messages.warning(request, "You need to log in to add items in your wishlist.")
    return redirect('login')


def wishlist_del(request,name,id):
    if request.user.is_authenticated:
                delete = lambda request,id: Wishlist.objects.get(user=request.user,listing_id=id).delete()
                back = lambda id : redirect('entry',name=Listing.objects.get(id=id).name,id=id)
                    
                if request.method == 'POST':
                    delete(request,id)
                
                if Wishlist.objects.filter(listing_id=id,user=request.user) and request.method != 'POST':
                   delete(request,id)
                   
                return back(id)
    messages.warning(request, "You need to log in to remove items from your wishlist.")
    return redirect('login')





class categoryform(forms.Form):
    category = forms.ChoiceField(
        choices=[
            
            ('electronics', 'Electronics'),
            ('books', 'Books'),
            ('fashion', 'Fashion'),
            ('home', 'Home & Garden'),
        ],
        initial='electronics',
        widget=forms.Select(attrs={
            'class':"form-select form-select-lg mb-3",
            
        })
    
    )



def category(request):
    if request.method == 'POST':
        ...
    return render(request,'auctions/categories.html',{
        'data': None,
        'form':categoryform(),
        'show':False
    })