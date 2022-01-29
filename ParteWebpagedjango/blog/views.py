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
from .models import Deportista, Post, Comensal, Dia1
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

"""
@login_required 
def Parte(request):
    vari = [[],[],[],[]]
    user = None
    etiquetas = [['respuestaLb','respuestaLl','respuestaLd','respuestaLm']]
    if request.user.is_authenticated:   #Este if no es necesario
        user = request.user.username #guarda el nombre de usuario
    try:    #Para obtener la respuesta anterior si la hay
        answer = Comensal.objects.get(user=user)    #query para sacar la respuesta anterior
        vari[0] = [answer.Lb, answer.Ll, answer.Ld, answer.Lm]
    except Comensal.DoesNotExist:
        vari[0] = ['-','-','-','-']

    if request.method=="POST":
        #for i in range(7):
        i=0
        vari[0]=[request.POST.get(etiquetas[i][0],''),request.POST.get(etiquetas[i][1],''),request.POST.get(etiquetas[i][2],''),request.POST.get(etiquetas[i][3],'')]
        #vari.append(request.POST.get('respuestaLl',''))
        #vari.append(request.POST.get('respuestaLd',''))
        #vari.append(request.POST.get('respuestaLm',''))

        try:
            answer = Comensal.objects.get(user=user)    #query para sacar la respuesta anterior
            answer.Lb=vari[0][0]
            answer.Ll=vari[0][1]
            answer.Ld=vari[0][2]
            answer.Lm=vari[0][3]


        except Comensal.DoesNotExist:
            answer = Comensal(user=user, Lb=vari[0][0], Ll=vari[0][1], Ld=vari[0][2], Lm=vari[0][3])
        answer.save() #guarda la nueva respuesta en la base de datos

    dias = ["Lunes"]#,"Martes","Miercoles","Jueves","Viernes","Sábado","Domingo"]
    num = [0]#, 1, 2, 3, 4, 5, 6]
    return render(request, 'blog/parte.html', {'vari': vari, 'dias': dias, 'num': num, 'etiquetas': etiquetas, 'title': 'Parte'})
"""

@login_required 
def Parte(request):
    vari = [[],[],[],[],[],[],[]]
    user = None
    etiquetas = [
    ['respuestaLb','respuestaLl','respuestaLd','respuestaLm'],
    ['respuestaMb','respuestaMl','respuestaMd','respuestaMm'],
    ['respuestaXb','respuestaXl','respuestaXd','respuestaXm'],
    ['respuestaJb','respuestaJl','respuestaJd','respuestaJm'],
    ['respuestaVb','respuestaVl','respuestaVd','respuestaVm'],
    ['respuestaSb','respuestaSl','respuestaSd','respuestaSm'],
    ['respuestaDb','respuestaDl','respuestaDd','respuestaDm'],
    ]
    if request.user.is_authenticated:   #Este if no es necesario
        user = request.user.username #guarda el nombre de usuario
    try:    #Para obtener la respuesta anterior si la hay
        answer = Comensal.objects.get(user=user)    #query para sacar la respuesta anterior
        vari[0] = [answer.L.b,answer.L.l,answer.L.d,answer.L.m]
        vari[1] = [answer.M.b,answer.M.l,answer.M.d,answer.M.m]
        vari[2] = [answer.X.b,answer.X.l,answer.X.d,answer.X.m]
        vari[3] = [answer.J.b,answer.J.l,answer.J.d,answer.J.m]
        vari[4] = [answer.V.b,answer.V.l,answer.V.d,answer.V.m]
        vari[5] = [answer.S.b,answer.S.l,answer.S.d,answer.S.m]
        vari[6] = [answer.D.b,answer.D.l,answer.D.d,answer.D.m]
    except Comensal.DoesNotExist:
        vari[0] = ['-','-','-','-']
        vari[1] = ['-','-','-','-']
        vari[2] = ['-','-','-','-']
        vari[3] = ['-','-','-','-']
        vari[4] = ['-','-','-','-']
        vari[5] = ['-','-','-','-']
        vari[6] = ['-','-','-','-']
    if request.method=="POST":
        for i in range(7):
            vari[i]=[request.POST.get(etiquetas[i][0],''),request.POST.get(etiquetas[i][1],''),request.POST.get(etiquetas[i][2],''),request.POST.get(etiquetas[i][3],'')]
        #vari.append(request.POST.get('respuestaLl',''))
        #vari.append(request.POST.get('respuestaLd',''))
        #vari.append(request.POST.get('respuestaLm',''))
        
        L = Dia1(b=vari[0][0],l=vari[0][1],d=vari[0][2],m=vari[0][3])
        M = Dia1(b=vari[1][0],l=vari[1][1],d=vari[1][2],m=vari[1][3])
        X = Dia1(b=vari[2][0],l=vari[2][1],d=vari[2][2],m=vari[2][3])
        J = Dia1(b=vari[3][0],l=vari[3][1],d=vari[3][2],m=vari[3][3])
        V = Dia1(b=vari[4][0],l=vari[4][1],d=vari[4][2],m=vari[4][3])
        S = Dia1(b=vari[5][0],l=vari[5][1],d=vari[5][2],m=vari[5][3])
        D = Dia1(b=vari[6][0],l=vari[6][1],d=vari[6][2],m=vari[6][3])
        L.save()
        M.save()
        X.save()
        J.save()
        V.save()
        S.save()
        D.save()
        try:
            answer = Comensal.objects.get(user=user)    #query para sacar la respuesta anterior
            answer.L = L
            answer.M = M
            answer.X = X
            answer.J = J
            answer.V = V
            answer.S = S
            answer.D = D
            
            """answer.L = Dia1(b=vari[0][0],l=vari[0][1],d=vari[0][2],m=vari[0][3]).save()
            answer.M = Dia1(b=vari[1][0],l=vari[1][1],d=vari[1][2],m=vari[1][3]).save()
            answer.X = Dia1(b=vari[2][0],l=vari[2][1],d=vari[2][2],m=vari[2][3]).save()
            answer.J = Dia1(b=vari[3][0],l=vari[3][1],d=vari[3][2],m=vari[3][3]).save()
            answer.V = Dia1(b=vari[4][0],l=vari[4][1],d=vari[4][2],m=vari[4][3]).save()
            answer.S = Dia1(b=vari[5][0],l=vari[5][1],d=vari[5][2],m=vari[5][3]).save()
            answer.D = Dia1(b=vari[6][0],l=vari[6][1],d=vari[6][2],m=vari[6][3]).save()
"""
        except Comensal.DoesNotExist:
            answer = Comensal(user=user,L=L,M=M,X=X,J=J,V=V,S=S,D=S)

            """answer = Comensal(user=user, 
                L=Dia1(b=vari[0][0],l=vari[0][1],d=vari[0][2],m=vari[0][3]).save(), 
                M=Dia1(b=vari[1][0],l=vari[1][1],d=vari[1][2],m=vari[1][3]).save(), 
                X=Dia1(b=vari[2][0],l=vari[2][1],d=vari[2][2],m=vari[2][3]).save(), 
                J=Dia1(b=vari[3][0],l=vari[3][1],d=vari[3][2],m=vari[3][3]).save(), 
                V=Dia1(b=vari[4][0],l=vari[4][1],d=vari[4][2],m=vari[4][3]).save(), 
                S=Dia1(b=vari[5][0],l=vari[5][1],d=vari[5][2],m=vari[5][3]).save(), 
                D=Dia1(b=vari[6][0],l=vari[6][1],d=vari[6][2],m=vari[6][3]).save())"""
        answer.save() #guarda la nueva respuesta en la base de datos

    dias = ["Lunes","Martes","Miercoles","Jueves","Viernes","Sábado","Domingo"]
#    num = [0, 1, 2, 3, 4, 5, 6]
#    dias = {'0':"Lunes", '1':"Martes", '2':"Miercoles", '3':"Jueves", '4':"Viernes", '5':"Sábado", '6':"Domingo"}
    variables = [[],[],[],[],[],[],[]]
    for i in range(7):
        variables[i] = [vari[i], dias[i], etiquetas[i]]

    return render(request, 'blog/parte.html', {'variables': variables, 'title': 'Parte'})

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
    return render(request, 'blog/deporte.html', {'dxt': dxt, 'title': 'Deporte'})

    