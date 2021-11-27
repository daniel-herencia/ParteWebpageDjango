from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='blog-home'),     #name => url name, to access it in other scripts without knowing the exact url
    path('about/', views.about, name='blog-about'),
    #path('prueba2/', views.prueba2, name='blog-pureba2'),
]
