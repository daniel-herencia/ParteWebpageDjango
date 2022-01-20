
from django.contrib import admin
from .models import Contact, Post, Deportista, Depor

admin.site.register(Post)   #To access post and edit them in the admin webpage
admin.site.register(Deportista)  #To save deporte in database
admin.site.register(Depor)
admin.site.register(Contact)
