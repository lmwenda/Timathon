from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

# Messages import
from django.contrib import messages

# Authentication, login and logout imports
from django.contrib.auth import authenticate, login, logout

# Form imports
from .forms import CreateUserForm, LoginUserForm

# Decorators imports e.g Login Required
from django.contrib.auth.decorators import login_required

# Send Mail imports and settings
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.

def index(response):
    return render(response, "main/index.html", {})

@login_required(login_url="login")
def generator(response):
	return render(response, "main/generator.html", {})

def login(request, user):
   
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('/')
		else:
			messages.info(request, 'Incorrect username or password. Try again.')	

	context = {}
	return render(request, "main/login.html", context)

def signup(request, user):
	if request.method == "POST":
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.cleaned_data('username')
			message.success(request, 'Your Account has Successfully been Created.')
		return redirect('/login')


	form = CreateUserForm()
	context = {'form':form}
	return render(request, "main/signup.html", context)