from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


def home(request):
    return render(request, "home.html")


@login_required
def index(request):
    return render(request, "home.html")


def login(request):
    return render(request, "registration/login.html")


def exit(request):
    logout(request)
    return redirect("home")
