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
from django_tex.shortcuts import render_to_pdf
from datetime import date   #Para saber la fecha
from datetime import datetime   #Para saber la fecha


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
        ops = answer.opciones
        vari[0] = [answer.L.b,answer.L.l,answer.L.d,answer.L.m]
        vari[1] = [answer.M.b,answer.M.l,answer.M.d,answer.M.m]
        vari[2] = [answer.X.b,answer.X.l,answer.X.d,answer.X.m]
        vari[3] = [answer.J.b,answer.J.l,answer.J.d,answer.J.m]
        vari[4] = [answer.V.b,answer.V.l,answer.V.d,answer.V.m]
        vari[5] = [answer.S.b,answer.S.l,answer.S.d,answer.S.m]
        vari[6] = [answer.D.b,answer.D.l,answer.D.d,answer.D.m]
    except Comensal.DoesNotExist:
        ops = 'Normal'
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
        ops = request.POST.get('opciones','')
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
            answer.opciones = ops
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
            answer = Comensal(user=user,opciones=ops,L=L,M=M,X=X,J=J,V=V,S=S,D=S)

            """answer = Comensal(user=user, 
                L=Dia1(b=vari[0][0],l=vari[0][1],d=vari[0][2],m=vari[0][3]).save(), 
                M=Dia1(b=vari[1][0],l=vari[1][1],d=vari[1][2],m=vari[1][3]).save(), 
                X=Dia1(b=vari[2][0],l=vari[2][1],d=vari[2][2],m=vari[2][3]).save(), 
                J=Dia1(b=vari[3][0],l=vari[3][1],d=vari[3][2],m=vari[3][3]).save(), 
                V=Dia1(b=vari[4][0],l=vari[4][1],d=vari[4][2],m=vari[4][3]).save(), 
                S=Dia1(b=vari[5][0],l=vari[5][1],d=vari[5][2],m=vari[5][3]).save(), 
                D=Dia1(b=vari[6][0],l=vari[6][1],d=vari[6][2],m=vari[6][3]).save())"""
        answer.save() #guarda la nueva respuesta en la base de datos

    dias = ["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"]
#    num = [0, 1, 2, 3, 4, 5, 6]
#    dias = {'0':"Lunes", '1':"Martes", '2':"Miercoles", '3':"Jueves", '4':"Viernes", '5':"Sábado", '6':"Domingo"}
    variables = [[],[],[],[],[],[],[]]
    for i in range(7):
        variables[i] = [vari[i], dias[i], etiquetas[i]]

    return render(request, 'blog/parte.html', {'variables': variables, 'title': 'Parte', 'opciones': ops})

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

@login_required
def parte_to_pdf(request):
    template_name = 'blog/tex/test.tex'
    today = date.today()
    dias = ["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"]
    meses = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
    num_day = today.weekday()
    dia = dias[num_day]
    tipo = {
		'enfermo': 0,
		'dieta': 0,
		'blando': 0,
		'item_author': 0,
        'cesta_enfermo': 0,
        'cesta_dieta': 0,
        'cesta_blando': 0,
        'fiambrera_enfermo': 0,
        'fiambrera_dieta': 0,
        'fiambrera_blando': 0
    }
    #NORMALES
    desayuno = {
        'Normal': 0,
        'Bocadillo-Pequeño': 0,
        '-': 0,
        'Bocadillo': 0,
        'Cesta': 0,
        'Fiambrera': 0
    }
    comida = {
        'Normal': 0,
        'Bocadillo-Pequeño': 0,
        '-': 0,
        'Bocadillo': 0,
        'Cesta': 0,
        'Fiambrera': 0,
        'Comida-13:00': 0,
        'Comida-13:30': 0,
        'Comida-14:00': 0
    }
    cena = {
        'Normal': 0,
        'Bocadillo-Pequeño': 0,
        '-': 0,
        'Bocadillo': 0,
        'Cesta': 0,
        'Fiambrera': 0
    }
    mediamañana = {
        '-': 0,
        'Si': 0
    }
    bocayfiambreras = {     #ESTO ES DE LA COMDIA DEL DIA SIGUIENTE
        'Bocadillo-Pequeño': 0,
        'Bocadillo': 0,
        'Fiambrera': 0
    }
    usuariosBocyF = {       #ESTO ES DE LA COMIDA DEL DIA SIGUIENTE
        'Bocadillo-Pequeño': [],
        'Bocadillo': [],
        'Fiambrera': []
    }
    #DIETA
    usuariosDieta = []
    desayunoD = {
        'Normal': 0,
        'Bocadillo-Pequeño': 0,
        '-': 0,
        'Bocadillo': 0,
        'Cesta': 0,
        'Fiambrera': 0
    }
    comidaD = {
        'Normal': 0,
        'Bocadillo-Pequeño': 0,
        '-': 0,
        'Bocadillo': 0,
        'Cesta': 0,
        'Fiambrera': 0,
        'Comida-13:00': 0,
        'Comida-13:30': 0,
        'Comida-14:00': 0
    }
    cenaD = {
        'Normal': 0,
        'Bocadillo-Pequeño': 0,
        '-': 0,
        'Bocadillo': 0,
        'Cesta': 0,
        'Fiambrera': 0
    }
    mediamañanaD = {
        '-': 0,
        'Si': 0
    }
    bocayfiambrerasD = {
        'Bocadillo-Pequeño': 0,
        'Bocadillo': 0,
        'Fiambrera': 0
    }
    usuariosBocyFD = {
        'Bocadillo-Pequeño': [],
        'Bocadillo': [],
        'Fiambrera': []
    }
    #ENFERMOS
    desayunoE = {
        'Normal': 0,
        'Bocadillo-Pequeño': 0,
        '-': 0,
        'Bocadillo': 0,
        'Cesta': 0,
        'Fiambrera': 0
    }
    comidaE = {
        'Normal': 0,
        'Bocadillo-Pequeño': 0,
        '-': 0,
        'Bocadillo': 0,
        'Cesta': 0,
        'Fiambrera': 0,
        'Comida-13:00': 0,
        'Comida-13:30': 0,
        'Comida-14:00': 0
    }
    cenaE = {
        'Normal': 0,
        'Bocadillo-Pequeño': 0,
        '-': 0,
        'Bocadillo': 0,
        'Cesta': 0,
        'Fiambrera': 0
    }
    mediamañanaE = {
        '-': 0,
        'Si': 0
    }
    bocayfiambrerasE = {
        'Bocadillo-Pequeño': 0,
        'Bocadillo': 0,
        'Fiambrera': 0
    }
    usuariosBocyFE = {
        'Bocadillo-Pequeño': [],
        'Bocadillo': [],
        'Fiambrera': []
    }
    #BLANDOS
    desayunoB = {
        'Normal': 0,
        'Bocadillo-Pequeño': 0,
        '-': 0,
        'Bocadillo': 0,
        'Cesta': 0,
        'Fiambrera': 0
    }
    comidaB = {
        'Normal': 0,
        'Bocadillo-Pequeño': 0,
        '-': 0,
        'Bocadillo': 0,
        'Cesta': 0,
        'Fiambrera': 0,
        'Comida-13:00': 0,
        'Comida-13:30': 0,
        'Comida-14:00': 0
    }
    cenaB = {
        'Normal': 0,
        'Bocadillo-Pequeño': 0,
        '-': 0,
        'Bocadillo': 0,
        'Cesta': 0,
        'Fiambrera': 0
    }
    mediamañanaB = {
        '-': 0,
        'Si': 0
    }
    bocayfiambrerasB = {
        'Bocadillo-Pequeño': 0,
        'Bocadillo': 0,
        'Fiambrera': 0
    }
    usuariosBocyFB = {
        'Bocadillo-Pequeño': [],
        'Bocadillo': [],
        'Fiambrera': []
    }

    #Para obtener la respuesta anterior si la hay
    #comensales = Comensal.objects.get()    #query para sacar las respuestas

    #for comensal in comensales.user:

    for com in Comensal.objects.all():
        try:
            comensal = com.user
            parte = Comensal.objects.get(user=comensal)
            if parte.opciones == 'Normal':
                if num_day == 0:
                    comida[parte.L.l]+=1
                    cena[parte.L.d]+=1
                    desayuno[parte.M.b]+=1
                    mediamañana[parte.M.m]+=1
                    if (parte.M.l == 'Fiambrera') or (parte.M.l == 'Bocadillo-Pequeño') or (parte.M.l == 'Bocadillo'):
                        bocayfiambreras[parte.M.l]+=1
                        usuariosBocyF[parte.M.l].append(comensal)
                elif num_day == 1:
                    comida[parte.M.l]+=1
                    cena[parte.M.d]+=1
                    desayuno[parte.X.b]+=1
                    mediamañana[parte.X.m]+=1
                    if (parte.X.l == 'Fiambrera') or (parte.X.l == 'Bocadillo-Pequeño') or (parte.X.l == 'Bocadillo'):
                        bocayfiambreras[parte.X.l]+=1
                        usuariosBocyF[parte.X.l].append(comensal)
                elif num_day == 2:
                    comida[parte.X.l]+=1
                    cena[parte.X.d]+=1
                    desayuno[parte.J.b]+=1
                    mediamañana[parte.J.m]+=1
                    if (parte.J.l == 'Fiambrera') or (parte.J.l == 'Bocadillo-Pequeño') or (parte.J.l == 'Bocadillo'):
                        bocayfiambreras[parte.J.l]+=1
                        usuariosBocyF[parte.J.l].append(comensal)
                elif num_day == 3:
                    comida[parte.J.l]+=1
                    cena[parte.J.d]+=1
                    desayuno[parte.V.b]+=1
                    mediamañana[parte.V.m]+=1
                    if (parte.V.l == 'Fiambrera') or (parte.V.l == 'Bocadillo-Pequeño') or (parte.V.l == 'Bocadillo'):
                        bocayfiambreras[parte.V.l]+=1
                        usuariosBocyF[parte.V.l].append(comensal)
                elif num_day == 4:
                    comida[parte.V.l]+=1
                    cena[parte.V.d]+=1
                    desayuno[parte.S.b]+=1
                    mediamañana[parte.S.m]+=1
                    if (parte.S.l == 'Fiambrera') or (parte.S.l == 'Bocadillo-Pequeño') or (parte.S.l == 'Bocadillo'):
                        bocayfiambreras[parte.S.l]+=1
                        usuariosBocyF[parte.S.l].append(comensal)
                elif num_day == 5:
                    comida[parte.S.l]+=1
                    cena[parte.S.d]+=1
                    desayuno[parte.D.b]+=1
                    mediamañana[parte.D.m]+=1
                    if (parte.D.l == 'Fiambrera') or (parte.D.l == 'Bocadillo-Pequeño') or (parte.D.l == 'Bocadillo'):
                        bocayfiambreras[parte.D.l]+=1
                        usuariosBocyF[parte.D.l].append(comensal)
                elif num_day == 6:
                    comida[parte.D.l]+=1
                    cena[parte.D.d]+=1
                    desayuno[parte.L.b]+=1
                    mediamañana[parte.L.m]+=1
                    if (parte.L.l == 'Fiambrera') or (parte.L.l == 'Bocadillo-Pequeño') or (parte.L.l == 'Bocadillo'):
                        bocayfiambreras[parte.L.l]+=1
                        usuariosBocyF[parte.L.l].append(comensal)

            elif parte.opciones == 'Dieta':
                tipo['dieta']+=1
                usuariosDieta.append(comensal)
                if num_day == 0:
                    comidaD[parte.L.l]+=1
                    cenaD[parte.L.d]+=1
                    desayunoD[parte.M.b]+=1
                    mediamañanaD[parte.M.m]+=1
                    if (parte.M.l == 'Fiambrera') or (parte.M.l == 'Bocadillo-Pequeño') or (parte.M.l == 'Bocadillo'):
                        bocayfiambrerasD[parte.M.l]+=1
                        usuariosBocyFD[parte.M.l].append(comensal)
                elif num_day == 1:
                    comidaD[parte.M.l]+=1
                    cenaD[parte.M.d]+=1
                    desayunoD[parte.X.b]+=1
                    mediamañanaD[parte.X.m]+=1
                    if (parte.X.l == 'Fiambrera') or (parte.X.l == 'Bocadillo-Pequeño') or (parte.X.l == 'Bocadillo'):
                        bocayfiambrerasD[parte.X.l]+=1
                        usuariosBocyFD[parte.X.l].append(comensal)
                elif num_day == 2:
                    comidaD[parte.X.l]+=1
                    cenaD[parte.X.d]+=1
                    desayunoD[parte.J.b]+=1
                    mediamañanaD[parte.J.m]+=1
                    if (parte.J.l == 'Fiambrera') or (parte.J.l == 'Bocadillo-Pequeño') or (parte.J.l == 'Bocadillo'):
                        bocayfiambrerasD[parte.J.l]+=1
                        usuariosBocyFD[parte.J.l].append(comensal)
                elif num_day == 3:
                    comidaD[parte.J.l]+=1
                    cenaD[parte.J.d]+=1
                    desayunoD[parte.V.b]+=1
                    mediamañanaD[parte.V.m]+=1
                    if (parte.V.l == 'Fiambrera') or (parte.V.l == 'Bocadillo-Pequeño') or (parte.V.l == 'Bocadillo'):
                        bocayfiambrerasD[parte.V.l]+=1
                        usuariosBocyFD[parte.V.l].append(comensal)
                elif num_day == 4:
                    comidaD[parte.V.l]+=1
                    cenaD[parte.V.d]+=1
                    desayunoD[parte.S.b]+=1
                    mediamañanaD[parte.S.m]+=1
                    if (parte.S.l == 'Fiambrera') or (parte.S.l == 'Bocadillo-Pequeño') or (parte.S.l == 'Bocadillo'):
                        bocayfiambrerasD[parte.S.l]+=1
                        usuariosBocyFD[parte.S.l].append(comensal)
                elif num_day == 5:
                    comidaD[parte.S.l]+=1
                    cenaD[parte.S.d]+=1
                    desayunoD[parte.D.b]+=1
                    mediamañanaD[parte.D.m]+=1
                    if (parte.D.l == 'Fiambrera') or (parte.D.l == 'Bocadillo-Pequeño') or (parte.D.l == 'Bocadillo'):
                        bocayfiambrerasD[parte.D.l]+=1
                        usuariosBocyFD[parte.D.l].append(comensal)
                elif num_day == 6:
                    comidaD[parte.D.l]+=1
                    cenaD[parte.D.d]+=1
                    desayunoD[parte.L.b]+=1
                    mediamañanaD[parte.L.m]+=1
                    if (parte.L.l == 'Fiambrera') or (parte.L.l == 'Bocadillo-Pequeño') or (parte.L.l == 'Bocadillo'):
                        bocayfiambrerasD[parte.L.l]+=1
                        usuariosBocyFD[parte.L.l].append(comensal)
            elif parte.opciones == 'Enfermo':
                tipo['enfermo']+=1
                if num_day == 0:
                    comidaE[parte.L.l]+=1
                    cenaE[parte.L.d]+=1
                    desayunoE[parte.M.b]+=1
                    mediamañanaE[parte.M.m]+=1
                    if (parte.M.l == 'Fiambrera') or (parte.M.l == 'Bocadillo-Pequeño') or (parte.M.l == 'Bocadillo'):
                        bocayfiambrerasE[parte.M.l]+=1
                        usuariosBocyFE[parte.M.l].append(comensal)
                elif num_day == 1:
                    comidaE[parte.M.l]+=1
                    cenaE[parte.M.d]+=1
                    desayunoE[parte.X.b]+=1
                    mediamañanaE[parte.X.m]+=1
                    if (parte.X.l == 'Fiambrera') or (parte.X.l == 'Bocadillo-Pequeño') or (parte.X.l == 'Bocadillo'):
                        bocayfiambrerasE[parte.X.l]+=1
                        usuariosBocyFE[parte.X.l].append(comensal)
                elif num_day == 2:
                    comidaE[parte.X.l]+=1
                    cenaE[parte.X.d]+=1
                    desayunoE[parte.J.b]+=1
                    mediamañanaE[parte.J.m]+=1
                    if (parte.J.l == 'Fiambrera') or (parte.J.l == 'Bocadillo-Pequeño') or (parte.J.l == 'Bocadillo'):
                        bocayfiambrerasE[parte.J.l]+=1
                        usuariosBocyFE[parte.J.l].append(comensal)
                elif num_day == 3:
                    comidaE[parte.J.l]+=1
                    cenaE[parte.J.d]+=1
                    desayunoE[parte.V.b]+=1
                    mediamañanaE[parte.V.m]+=1
                    if (parte.V.l == 'Fiambrera') or (parte.V.l == 'Bocadillo-Pequeño') or (parte.V.l == 'Bocadillo'):
                        bocayfiambrerasE[parte.V.l]+=1
                        usuariosBocyFE[parte.V.l].append(comensal)
                elif num_day == 4:
                    comidaE[parte.V.l]+=1
                    cenaE[parte.V.d]+=1
                    desayunoE[parte.S.b]+=1
                    mediamañanaE[parte.S.m]+=1
                    if (parte.S.l == 'Fiambrera') or (parte.S.l == 'Bocadillo-Pequeño') or (parte.S.l == 'Bocadillo'):
                        bocayfiambrerasE[parte.S.l]+=1
                        usuariosBocyFE[parte.S.l].append(comensal)
                elif num_day == 5:
                    comidaE[parte.S.l]+=1
                    cenaE[parte.S.d]+=1
                    desayunoE[parte.D.b]+=1
                    mediamañanaE[parte.D.m]+=1
                    if (parte.D.l == 'Fiambrera') or (parte.D.l == 'Bocadillo-Pequeño') or (parte.D.l == 'Bocadillo'):
                        bocayfiambrerasE[parte.D.l]+=1
                        usuariosBocyFE[parte.D.l].append(comensal)
                elif num_day == 6:
                    comidaE[parte.D.l]+=1
                    cenaE[parte.D.d]+=1
                    desayunoE[parte.L.b]+=1
                    mediamañanaE[parte.L.m]+=1
                    if (parte.L.l == 'Fiambrera') or (parte.L.l == 'Bocadillo-Pequeño') or (parte.L.l == 'Bocadillo'):
                        bocayfiambrerasE[parte.L.l]+=1
                        usuariosBocyFE[parte.L.l].append(comensal)
            elif parte.opciones == 'Blando':
                tipo['blando']+=1
                if num_day == 0:
                    comidaB[parte.L.l]+=1
                    cenaB[parte.L.d]+=1
                    desayunoB[parte.M.b]+=1
                    mediamañanaB[parte.M.m]+=1
                    if (parte.M.l == 'Fiambrera') or (parte.M.l == 'Bocadillo-Pequeño') or (parte.M.l == 'Bocadillo'):
                        bocayfiambrerasB[parte.M.l]+=1
                        usuariosBocyFB[parte.M.l].append(comensal)
                elif num_day == 1:
                    comidaB[parte.M.l]+=1
                    cenaB[parte.M.d]+=1
                    desayunoB[parte.X.b]+=1
                    mediamañanaB[parte.X.m]+=1
                    if (parte.X.l == 'Fiambrera') or (parte.X.l == 'Bocadillo-Pequeño') or (parte.X.l == 'Bocadillo'):
                        bocayfiambrerasB[parte.X.l]+=1
                        usuariosBocyFB[parte.X.l].append(comensal)
                elif num_day == 2:
                    comidaB[parte.X.l]+=1
                    cenaB[parte.X.d]+=1
                    desayunoB[parte.J.b]+=1
                    mediamañanaB[parte.J.m]+=1
                    if (parte.J.l == 'Fiambrera') or (parte.J.l == 'Bocadillo-Pequeño') or (parte.J.l == 'Bocadillo'):
                        bocayfiambrerasB[parte.J.l]+=1
                        usuariosBocyFB[parte.J.l].append(comensal)
                elif num_day == 3:
                    comidaB[parte.J.l]+=1
                    cenaB[parte.J.d]+=1
                    desayunoB[parte.V.b]+=1
                    mediamañanaB[parte.V.m]+=1
                    if (parte.V.l == 'Fiambrera') or (parte.V.l == 'Bocadillo-Pequeño') or (parte.V.l == 'Bocadillo'):
                        bocayfiambrerasB[parte.V.l]+=1
                        usuariosBocyFB[parte.V.l].append(comensal)
                elif num_day == 4:
                    comidaB[parte.V.l]+=1
                    cenaB[parte.V.d]+=1
                    desayunoB[parte.S.b]+=1
                    mediamañanaB[parte.S.m]+=1
                    if (parte.S.l == 'Fiambrera') or (parte.S.l == 'Bocadillo-Pequeño') or (parte.S.l == 'Bocadillo'):
                        bocayfiambrerasB[parte.S.l]+=1
                        usuariosBocyFB[parte.S.l].append(comensal)
                elif num_day == 5:
                    comidaB[parte.S.l]+=1
                    cenaB[parte.S.d]+=1
                    desayunoB[parte.D.b]+=1
                    mediamañanaB[parte.D.m]+=1
                    if (parte.D.l == 'Fiambrera') or (parte.D.l == 'Bocadillo-Pequeño') or (parte.D.l == 'Bocadillo'):
                        bocayfiambrerasB[parte.D.l]+=1
                        usuariosBocyFB[parte.D.l].append(comensal)
                elif num_day == 6:
                    comidaB[parte.D.l]+=1
                    cenaB[parte.D.d]+=1
                    desayunoB[parte.L.b]+=1
                    mediamañanaB[parte.L.m]+=1
                    if (parte.L.l == 'Fiambrera') or (parte.L.l == 'Bocadillo-Pequeño') or (parte.L.l == 'Bocadillo'):
                        bocayfiambrerasB[parte.L.l]+=1
                        usuariosBocyFB[parte.L.l].append(comensal)
        except Comensal.DoesNotExist:
            a = 1

    #parte = Comensal.objects.get(user='parteadmin')
    #letra = 'L'
    #comida[parte.L.l]+=1
    #observaciones = comida[parte.L.l]
    observaciones = 'Adios'
    if request.method=="POST":
        observaciones = request.POST.get('observaciones', '')
    context = {'title': 'Parte en PDF', 'tipo': tipo, 'observaciones': observaciones, 'numerodia': today.day, 'mes': meses[today.month],
     'año': today.year, 'dia':dia,
     'comida': comida, 'cena': cena, 'desayuno': desayuno, 'mediamañana': mediamañana, 'bocayfiambreras': bocayfiambreras, 'usuariosBocyF': usuariosBocyF,
     'comidaD': comidaD, 'cenaD': cenaD, 'desayunoD': desayunoD, 'mediamañanaD': mediamañanaD, 'bocayfiambrerasD': bocayfiambrerasD, 'usuariosBocyFD': usuariosBocyFD,
     'comidaB': comidaB, 'cenaB': cenaB, 'desayunoB': desayunoB, 'mediamañanaB': mediamañanaB, 'bocayfiambrerasB': bocayfiambrerasB, 'usuariosBocyFB': usuariosBocyFB,
     'comidaE': comidaE, 'cenaE': cenaE, 'desayunoE': desayunoE, 'mediamañanaE': mediamañanaE, 'bocayfiambrerasE': bocayfiambrerasE, 'usuariosBocyFE': usuariosBocyFE,
     'usuariosDieta': usuariosDieta}

    return render_to_pdf(request, template_name, context, filename='PartePDF.pdf')

#        return render_to_pdf(request, template_name, "ERROR!!!",filename='PartePDF.pdf')


@login_required
def parte_to_pdf2(request):
    template_name = 'blog/tex/parte2.tex'
    today = date.today()
    dias = ["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"]
    meses = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
    num_day = today.weekday()
    dia = dias[num_day]
    usuarios = []
    """
    partesL1 = []
    partesD1 = []
    partesB2 = []
    partesL2 = []
    partesD2 = []
    partesM = []
    """
    partesDia1 = []
    partesDia2 = []


    for com in Comensal.objects.all():
        usuarios.append(com.user)
        if num_day == 0:
            """
            partesL1.append()
            partesD1.append()
            partesB2.append()
            partesL2.append()
            partesD2.append()
            partesM.append()
            """
            partesDia1.append(com.L)
            partesDia2.append(com.M)
        elif num_day == 1:
            partesDia1.append(com.M)
            partesDia2.append(com.X)
        elif num_day == 2:
            partesDia1.append(com.X)
            partesDia2.append(com.J)
        elif num_day == 3:
            partesDia1.append(com.J)
            partesDia2.append(com.V)
        elif num_day == 4:
            partesDia1.append(com.V)
            partesDia2.append(com.S)
        elif num_day == 5:
            partesDia1.append(com.S)
            partesDia2.append(com.D)
        elif num_day == 6:
            partesDia1.append(com.D)
            partesDia2.append(com.L)
        
    context = {'title': 'Parte en PDF', 'usuarios': usuarios, 'partesDia1': partesDia1, 'partesDia2': partesDia1, 'numerodia': today.day, 'mes': meses[today.month],
     'año': today.year, 'dia':dia}

    return render_to_pdf(request, template_name, context, filename='PartePDF2.pdf')


@login_required
def Imprimir(request):
    if  request.user.username == 'parteadmin':
        return render(request, 'blog/imprimir.html', {'title': 'Imprimir'})
    else:
        return render(request, 'blog/parte.html', {'title': 'Parte'})
