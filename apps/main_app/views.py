from django.shortcuts import render, redirect
from models import Quote
from ..login_app.models import User
from django.contrib import messages


# Create your views here.
def dashboard(request):
    context = {
        'cur_user': User.objects.get(id = request.session['id']),
        'favorite_quotes': Quote.objects.filter(favorites = request.session['id']),
        'other_quotes': Quote.objects.exclude(favorites = request.session['id']),
    }
    if 'email' not in request.session:
        return redirect('/')
    return render(request, 'main_app/dashboard.html', context)

def add(request):
    results = Quote.objects.validate(request.POST)
    if results['status'] == True:
        logged_user = User.objects.get(id = request.session['id'])
        new_quote = Quote.objects.create(
            quoted_by = request.POST['quoted_by'],
            quote = request.POST['quote'],
            posted_by = User.objects.get(id=request.session['id'])
        )
        User.objects.get(id = request.session['id']).posted_by.add(new_quote)
        # User.objects.get(id = request.session['id']).favorites.add(new_quote)

    else:
        for error in results['errors']:
            messages.error(request, error)

    return redirect('/main/dashboard')


def addtofavorites (request, id):
    to_add = Quote.objects.get(id = id)
    user = User.objects.get(id = request.session['id'])
    user.favorites.add(to_add)
    return redirect('/main/dashboard')

def removefromfavorites (request, id):
    to_remove = Quote.objects.get(id = id)
    user = User.objects.get(id = request.session['id'])
    user.favorites.remove(to_remove)
    return redirect('/main/dashboard')

def show(request, id):
    context = {
        'quote': Quote.objects.get(id = id),
        'quoted_by': Quote.objects.filter(quoted_by = request.session['id']),
    }
    return render(request, 'main_app/show.html', context)