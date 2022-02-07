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
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('', views.Inicio, name='blog-inicio'),
    path('blog/', login_required(PostListView.as_view()), name='blog-home'),
    path('user/<str:username>', login_required(UserPostListView.as_view()), name='user-posts'),
    path('post/<int:pk>/', login_required(PostDetailView.as_view()), name='post-detail'),
    path('post/new/', login_required(PostCreateView.as_view()), name='post-create'),
    path('post/<int:pk>/update/', login_required(PostUpdateView.as_view()), name='post-update'),
    path('post/<int:pk>/delete/', login_required(PostDeleteView.as_view()), name='post-delete'),
    path('parte/', views.Parte, name='blog-parte'),
#    path('deporte/', views.Deporte, name='blog-deporte'),
    path('deporte/', views.deportista, name='blog-deporte'),
    path('enlaces/', views.Enlaces, name='blog-enlaces'),
    path('extras/', views.Extras, name='blog-extras'),
    path('imprimir/', views.Imprimir, name='blog-imprimir'),
    path('partepdf/', views.parte_to_pdf, name='parte_to_pdf'),
    path('partepdf2/', views.parte_to_pdf2, name='parte_to_pdf2'),
    path('modificar/', views.Modificar, name='blog-modificar')
#    path("contact/", views.contact, name="blog-contact"),

]
#<app>/<model>_<viewtype>.html