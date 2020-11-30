from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
import bcrypt

def index(request):
    return render(request, "index.html")

def register(request):
    error = User.objects.basic_validator(request.POST)
    if len(error) > 0:
        for message in error.values():
            messages.error(request, message)
        return redirect('/')
    password = request.POST['password']
    pw_hash = bcrypt.hashpw(request.POST['password'].encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    new_user = User.objects.create(
        first_name=request.POST['first_name'],
        last_name=request.POST['last_name'],
        email=request.POST['email'],
        password= pw_hash
    )
    request.session['user_id'] = new_user.id
    return redirect('/success')

def login(request):
    error = User.objects.login_validator(request.POST)
    if len(error) > 0:
        for message in error.values():
            messages.error(request, message)
        return redirect('/')
    list_of_users = User.objects.filter(email=request.POST['email'])
    if len(list_of_users) > 0:
        user = list_of_users[0]
        if bcrypt.checkpw(request.POST['password'].encode("utf-8"), user.password.encode("utf-8")):
            request.session['user_id'] = user.id
            return redirect('/success')
    return redirect('/')

def success(request):
    if 'user_id' not in request.session:
        return redirect('/')
    logged_in_user = User.objects.get(id=request.session['user_id'])
    print(logged_in_user.__dict__)
    context = {
        'logged_in_user': logged_in_user
    }
    return render(request, "success.html", context)

def logout(request):
    request.session.clear()
    return redirect('/')




# Create your views here.
