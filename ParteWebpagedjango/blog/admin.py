
from django.contrib import admin
from .models import Post, Deportista

admin.site.register(Post)   #To access post and edit them in the admin webpage
admin.site.register(Deportista)  #To save deporte in database
#admin.site.register(Contact)
