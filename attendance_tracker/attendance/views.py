from django.urls import reverse
from .models import User, subject
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout 

def index(request):
    if request.user.is_authenticated:
        return render(request, 'attendance/index.html',{
            'username':request.user.username,
            'subjects':subject.objects.all(),
        })
    return render(request, 'attendance/index.html')

def user_signup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "attendance/signup.html", {
                "message": "Passwords must match!"
            })

        try:
            if username == "":
                return render(request, "attendance/signup.html",{
                    "message": "Username cannot be empty!"
                })
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "attendance/signup.html", {
                "message": "Username already taken!"
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "attendance/signup.html")

def user_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "attendance/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "attendance/login.html")

def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def add_sub(request):
    if request.user.is_authenticated:
        if request.method=='GET':
            return render(request,"attendance/add_sub.html")
        if request.method=='POST':
            subname=request.POST.get('subname')
            initotal=request.POST.get('initotal')
            inipresent=request.POST.get('inipresent')
            sub=subject(sub_name=subname,user=request.user,totalclasses=initotal,present=inipresent)
            sub.save()
            return HttpResponseRedirect(reverse("index"))

def inc_att(request,id):
    sub=subject.objects.get(id=id)
    sub.present+=1
    sub.totalclasses+=1
    sub.save()
    return HttpResponseRedirect(reverse("index"))

def dec_att(request,id):
    sub=subject.objects.get(id=id)
    sub.totalclasses+=1
    sub.save()
    return HttpResponseRedirect(reverse("index"))