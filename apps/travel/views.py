from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from  datetime import datetime
import bcrypt
import re
from django.db.models import Q
from .models import *

# Create your views here.
def index(request):
  return render(request, "travel/index.html")

def check_password(request, username, password):
      u = User.objects.filter(username=username).first()
      if u == None:
          messages.add_message(request, messages.ERROR, "Not registered, please register!")
          return 1
      hashed = u.password
      if bcrypt.hashpw(password.encode("utf-8"), hashed.encode("utf-8")) == hashed.encode("utf-8"):
        print "It matches"
        return u
      else:
        messages.add_message(request, messages.ERROR, "Password not matched!")
        print "It does not match"
        return 2

def login(request):
    error = None
    if len(request.POST['login_username']) < 3:
       error="error"
       messages.add_message(request, messages.ERROR, 'username has to be at least 3 characters! ')
    if len(request.POST['login_password']) < 8:
        messages.add_message(request, messages.ERROR, 'Password has to be at least 8 characters! ')
        error="error"
    if error == "error":
        context = {
            "category": "login"
        }
        return render(request, 'travel/index.html', context)
    user = check_password(request=request, username= request.POST['login_username'],
                          password=request.POST['login_password'])
    if user == 1 or user == 2:
        context = {
            "category": "login"
        }
        return render(request, 'travel/index.html', context)
    #if user != None:
    request.session['user_id'] = user.id
    name = user.name.split()
    request.session['first_name'] = name[0]
    request.session['username'] = user.username
    return redirect("/show_dashboard")

def show_dashboard(request):
    user = User.objects.get(id=request.session['user_id'])
    mytrips = Trip.objects.filter(turists=user)
    notmytrips = Trip.objects.exclude(turists=user)
    context = {
      "mytrips": mytrips,
      "notmytrips": notmytrips
    }
    return render(request, 'travel/dashboard.html', context)

def registration(request):
        error = None
        name = request.POST['name']
        username = request.POST['username']
        password = request.POST['password']
        if len(name) < 3:
           error="error"
           messages.add_message(request, messages.ERROR, 'name has to be at least 3 letters! ')
        if len(username) < 3:
           error="error"
           messages.add_message(request, messages.ERROR, 'username has to be at least 3 characters! ')
        if len(password) < 8:
           messages.add_message(request, messages.ERROR, 'Password has to be at least 8 characters! ')
           error="error"
        confirm_password = request.POST['password_confirm']
        if password != confirm_password:
           error="error"
           messages.add_message(request, messages.ERROR, 'Password and Confirm Password do not match! ')
        if error == None:
            if User.objects.filter(username=username).first():
                context = {
                    "category": "register"
                }
                messages.add_message(request, messages.ERROR, 'user exists! Please log in! ')
                return render(request, 'travel/index.html', context)
            passwd_encoded = password.encode('utf-8')
            hashed = bcrypt.hashpw(passwd_encoded, bcrypt.gensalt())
            user = User.objects.create(name=name, username=username, password=hashed)
            request.session['user_id'] = user.id
            request.session['username'] = username
            name = request.POST['name'].split()
            request.session['first_name'] = name[0]
            return redirect("/show_dashboard")
        else:
            context = {
                "category": "register"
            }
            return render(request, 'travel/index.html', context)

def create_plan(request):
    return render(request, 'travel/create_plan.html')

def join(request, id):
    u =  User.objects.get(id=request.session['user_id'])
    trip = Trip.objects.get(id=id)
    trip.turists.add(u)
    return redirect("/show_dashboard")

def create(request):
    error = None
    today = datetime.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    if len( request.POST['destination']) < 3:
       error="error"
       messages.add_message(request, messages.ERROR, 'destination has to be at least 3 letters! ')
    if len( request.POST['description']) < 3:
       error="error"
       messages.add_message(request, messages.ERROR, 'description has to be at least 3 letters! ')
    if request.POST['from_date'] == "":
       error="error"
       messages.add_message(request, messages.ERROR, 'Please enter from date! ')
    if request.POST['from_date'] != "" and request.POST['from_date'] < str(today):
       error="error"
       messages.add_message(request, messages.ERROR, 'from date has to be the future date!')
    if request.POST['to_date'] == "":
       error="error"
       messages.add_message(request, messages.ERROR, 'Please enter end date! ')
    if request.POST['to_date'] != "" and request.POST['to_date'] < str(today):
       error="error"
       messages.add_message(request, messages.ERROR, 'to date has to be the future date!')
    if request.POST['from_date'] != "" and request.POST['to_date'] != "" and request.POST['to_date'] < request.POST['from_date']:
       error="error"
       messages.add_message(request, messages.ERROR, 'from date has to be before to date!')
    if error != None:
       return redirect("/create_plan")
    planner =  User.objects.get(id=request.session['user_id'])
    trip = Trip.objects.create(destination=request.POST['destination'], description=request.POST['description'], planner=planner,
                    from_date=request.POST['from_date'], to_date=request.POST['to_date'], created_at=datetime.date.today)
    trip.turists.add(planner)
    trip.save()
    return redirect("/show_dashboard")


def show_trip(request, id):
    Context  = {
        "trip": Trip.objects.get(id=id)
    }
    return render(request, 'travel/show_trip.html', Context)

def logoff(request):
    try:
        del request.session['user_id']
        del request.session['username']
    except KeyError:
        pass
    return redirect('/')
