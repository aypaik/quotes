from django.shortcuts import render, redirect
from models import User
from ..main_app.models import Quote
from django.contrib import messages

# Create your views here.

def index(request):
    # User.objects.all().delete()
    # Quote.objects.all().delete()
    # ^---used to clear all saved users
    return render(request, 'login_app/index.html')

def register(request):
    results = User.objects.validate(request.POST)
    if results['status'] == True:
        user = User.objects.creator(request.POST)
        messages.success(request, 'User has been created.')
    else:
        for error in results['errors']:
            messages.error(request, error)

    return redirect('/')

def login(request):
    results = User.objects.loginVal(request.POST)
    if results['status'] == False:
        messages.error(request, 'Please check your email and password and try again.')
        return redirect('/')
    else:
        request.session['email'] = results['user'].email
        request.session['name'] = results['user'].name
        request.session['id'] = results['user'].id
        return redirect('/main/dashboard')

def logout(request):
    request.session.flush()
    return redirect('/')