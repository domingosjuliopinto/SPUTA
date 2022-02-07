from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request, 'home/base.html')

def loginUser(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect('/')
        else:
            messages.error(request, "Wrong Credentials")
            return render(request, 'home/login.html')
    else: 
        return render(request, 'home/login.html')
    
def logoutUser(request):
    logout(request)
    messages.success(request, "successfully logged out")
    return redirect('/')