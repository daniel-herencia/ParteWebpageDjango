import sqlite3
from turtle import end_fill
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Deportista, Post, Depor, Contact
from django.contrib import messages
from django.contrib.auth.decorators import login_required



#Logic of html files

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 4 #Number of post per page


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 4 #Number of post per page

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def Parte(request):
    return render(request, 'blog/parte.html', {'title': 'Parte'})

def Deporte(request):
    return render(request, 'blog/deporte.html', {'title': 'Deporte'})

def Saveitem(request):
    if request.method=="POST":
        name = request.POST.get('name', '')
        #respuesta = request.POST.get('respuesta', '')
        #savevalue = Deportista(name=name, respuesta=respuesta)
        savevalue = Deportista(name=name)
        savevalue.save()
    return render(request, 'blog/deporte.html')
        #if request.POST.get('respuesta'):
        #    savevalue=Deportista()
        #    savevalue.respuesta=request.POST.get('respuesta')
        #    savevalue.save()
        #    messages.success(request,'hola')
        #    #messages.success(request,'The Selected answer: '+savevalue.respuesta+' is saved successfully')
        #    return render(request,'deporte.html')
        #else:
        #    messages.success(request,'adios') 
        #    return render(request,'deporte.html')

class DeporDetailView(DetailView):
    model = Depor

class DeporCreateView(LoginRequiredMixin, CreateView):
    model = Depor
    fields = ['hace', 'author']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

@login_required 
def contact(request):
    thank = False
    if request.method=="POST":
        name = request.POST.get('name', '')
        user = None
        if request.user.is_authenticated:   #Este if no es necesario
           user = request.user.username #guarda el nombre de usuario
        #eliminado = Contact(name='',user=user)
        #eliminado.delete()

        #HABRIA QUE PONER UN LOG O ALGO PARA CONTROLAR QUE NO DEVUELVE MAS DE UN OBJETO LA SIGUIENTE QUERY!!!
        anterior= Contact.objects.get(user=user)    #query para sacar la respuesta anterior
#        email = request.POST.get('email', '')
#        phone = request.POST.get('phone', '')
#        desc = request.POST.get('desc', '')
#        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        anterior.name=name
        anterior.save() #guarda la nueva respuesta en la base de datos
        #contact = Contact(name=name, user=user)
        #contact.save()
        thank = True
    return render(request, 'blog/contact.html', {'thank': thank})

