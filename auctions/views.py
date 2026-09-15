from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
from auctions.models import *
from .models import User
from django import forms
import requests


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
            response = requests.get(image_url,timeout=2)

            content = response.headers.get("content-type","")
            if not content.startswith("image/"):
                raise forms.ValidationError("Must be a image")
        except requests.RequestException:
            return temp_url

        return image_url



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
            price = form.cleaned_data["price"]
            img = form.cleaned_data["image"]
            Listings.objects.create(name=name,price=price,image=img)
            return redirect('index')
        
        return render(request,'auctions/Add_listing.html',
                      {
                        'form':Createlisting(),
                        'warning':"Invalid image url"
                        }
                    )
    return render(request,'auctions/Add_listing.html',{
        'form':Createlisting()
    })