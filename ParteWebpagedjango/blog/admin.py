
from django.contrib import admin
from .models import Post, Deportista, Comensal, Recurso, Impresor, VariablesGlobales#, Dia

admin.site.register(Post)   #To access post and edit them in the admin webpage
admin.site.register(Deportista)  #To save deporte in database
admin.site.register(Comensal)
admin.site.register(Recurso)
admin.site.register(Impresor)
admin.site.register(VariablesGlobales)
#admin.site.register(Dia)
#admin.site.register(Contact)
