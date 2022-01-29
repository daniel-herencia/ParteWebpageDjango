from django.contrib import admin
from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
)
from . import views

urlpatterns = [
    path('', views.Inicio, name='blog-inicio'),
    path('blog/', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('parte/', views.Parte, name='blog-parte'),
#    path('deporte/', views.Deporte, name='blog-deporte'),
    path('deporte/', views.deportista, name='blog-deporte'),
    path('enlaces/', views.Enlaces, name='blog-enlaces'),
    path('extras/', views.Extras, name='blog-extras'),
    path('imprimir/', views.Imprimir, name='blog-imprimir'),
    path('partepdf/', views.parte_to_pdf, name='parte_to_pdf')
#    path("contact/", views.contact, name="blog-contact"),

]
#<app>/<model>_<viewtype>.html