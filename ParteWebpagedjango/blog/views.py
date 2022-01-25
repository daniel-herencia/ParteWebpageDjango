import sqlite3
#from turtle import end_fill
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
import sys
sys.path.append("..")# Adds higher directory to python modules path.
#from ..ParteWebpagedjango.settings import EMAIL_HOST_USER
from ParteWebpagedjango.settings import EMAIL_HOST_USER
from .models import Deportista, Post
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.utils.html import strip_tags


#Logic of html files

@login_required 
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
    success_url = '/blog/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

@login_required 
def Parte(request):
    return render(request, 'blog/parte.html', {'title': 'Parte'})

def Inicio(request):
    context = {
        'users': User.objects.all()
    }
    return render(request, 'blog/inicio.html', context)

@login_required 
def Enlaces(request):
    return render(request, 'blog/enlaces.html', {'title': 'Enlaces'})

@login_required 
def Extras(request):
    #current_user = request.user.username
    if  request.user.username == 'parteadmin':
        if request.method=="POST": 
            usuarios = User.objects.all()
            for usuario in usuarios:
                destinatario = usuario.email
                try:    #Para obtener la respuesta si la hay
                    answer = Deportista.objects.get(user=usuario.username).dxt
                except Deportista.DoesNotExist:
                    answer = 'N'

                if answer == 'S':
                    answer = 'SI haces deporte.'
                else:
                    answer = 'NO haces deporte.'
                html = """<html>
                            <body>
                                    <h4>¡Buenos días!</h4>
                                    <h4></h4>
                                    <h4>Esta semana </h4><h3>""" + answer + """</h3><br>
                                    <h4>¿Quieres enviar otra respuesta? Entra en el siguiente enlace: https://partebarcelona.pythonanywhere.com/deporte/</h4>
                                    <h4>No contestar a este correo, se ha generado automáticamente.</h4>
                                    <h4>Atentamente,</h4>
                                    <h4></h4>
                                    <h4>ParteProgrammingTeam</h4>
                            </body>
                            </html> """

                mensaje = strip_tags(html)
                send_mail('Correo semanal de Deporte',
                mensaje,
                EMAIL_HOST_USER,
                [destinatario],
                fail_silently=False)
        return render(request, 'blog/extras.html', {'title': 'Extras'})
    else:
        return render(request, 'blog/parte.html', {'title': 'Parte'})



#def Deporte(request):
#    return render(request, 'blog/deporte.html', {'title': 'Deporte'})

@login_required 
def deportista(request):
    user = None
    if request.user.is_authenticated:   #Este if no es necesario
        user = request.user.username #guarda el nombre de usuario
    try:    #Para obtener la respuesta anterior si la hay
        answer = Deportista.objects.get(user=user)    #query para sacar la respuesta anterior
        dxt=answer.dxt
    except Deportista.DoesNotExist:
        dxt='O'
    #Si se ha enviado una respuesta nueva:
    if request.method=="POST":  
        observaciones = request.POST.get('observaciones', '')
        dxt = request.POST.get('respuesta','')
        #Si por algun motivo hubiera dos respuestas de un mismo usuario seguramente petaria
        try:
            answer = Deportista.objects.get(user=user)    #query para sacar la respuesta anterior
            answer.observaciones=observaciones
            answer.dxt=dxt
        except Deportista.DoesNotExist:
            answer = Deportista(user=user, observaciones=observaciones, dxt=dxt)
        answer.save() #guarda la nueva respuesta en la base de datos
    return render(request, 'blog/deporte.html', {'dxt': dxt})

#@login_required 
#def contact(request):
#    thank = False
#    if request.method=="POST":
#        observaciones = request.POST.get('observaciones', '')
#        user = None
#        dxt = request.POST.get('respuesta','')
#        if request.user.is_authenticated:   #Este if no es necesario
#           user = request.user.username #guarda el nombre de usuario
#        #eliminado = Contact(name='',user=user)
#        #eliminado.delete()
#
#        #HABRIA QUE PONER UN LOG O ALGO PARA CONTROLAR QUE NO DEVUELVE MAS DE UN OBJETO LA SIGUIENTE QUERY!!!
#        anterior= Contact.objects.get(user=user)    #query para sacar la respuesta anterior
#        #email = request.POST.get('email', '')
#        #phone = request.POST.get('phone', '')
#        #desc = request.POST.get('desc', '')
#        #contact = Contact(name=name, email=email, phone=phone, desc=desc)
#        anterior.observaciones=observaciones
#        anterior.dxt=dxt
#        anterior.save() #guarda la nueva respuesta en la base de datos
#        #contact = Contact(name=name, user=user)
#        #contact.save()
#        thank = True
#    return render(request, 'blog/contact.html', {'thank': thank})

#contact.html
#{% extends "blog/base.html" %}

#{% block content %}

#<div class="container my-3">
#    <h1>Deporte</h1>
#    <h4>¿Haces deporte?</h4>
#    <form method="post" action="{% url 'blog-contact' %}">{% csrf_token %}
#        <div class="input-group">
#            <select class="custom-select" id="inputGroupSelect04" name='respuesta'>
#                <option selected>-- Selecciona una opción --</option>
#                <option value="S">Sí, hago deporte</option>
#                <option value="N">No hago deporte</option>
#            </select>
#        </div>
#        <br>
#        <div class="form-group">
#            <label for="name">Observaciones:</label>
#            <input type="text" class="form-control" id="name" name='observaciones' placeholder="Escribe aquí si tienes algo importante a tener en cuenta">
#        </div>
#        <hr/>
#        <button type="submit" class="btn btn-success">Submit</button>
#    </form>
#</div>

#{% endblock %}
#{% block js%}
#<script>
#{% if thank %}
#alert('Thanks for contacting us. We will get back to you soon!');

#document.location = "/blog/contact";
#{% endif %}
#</script>
#{% endblock %}

#base.html
#                  <!--<a class="nav-item nav-link" href="{% url 'blog-contact' %}">Contact</a>-->
#                  <!--<a class="nav-item nav-link" href="{% url 'login' %}">Contact</a>-->
