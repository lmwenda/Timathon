from django.contrib import admin
from .models import post, Admins_Post

# Register your models here.

admin.site.register(post)
admin.site.register(Admins_Post)