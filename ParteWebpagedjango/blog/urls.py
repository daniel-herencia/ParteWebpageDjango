from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('about/', views.about, name='blog-about'),
    #path('prueba2/', views.prueba2, name='blog-pureba2'),
]
