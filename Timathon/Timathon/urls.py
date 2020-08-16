from django.urls import path
from . import views

# Create your urls here.

urlpatterns = [
path("", views.index, name="index"),
path("generator/", views.generator, name="generator"),
path("login/", views.login, name="login"),
path("signup/", views.signup, name="signup")

]