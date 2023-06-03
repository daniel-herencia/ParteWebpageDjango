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
from .models import Deportista, Post, Comensal, Dia1, VariablesGlobales, Recurso, Impresor
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django_tex.shortcuts import render_to_pdf
from datetime import date   #Para saber la fecha
from datetime import datetime, timedelta   #Para saber la fecha
import decimal
#Email with dynamic content
from django.core import mail
from django.template.loader import render_to_string

#Para almacenar archivos
from django.conf import settings
from django.core.files.storage import FileSystemStorage


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
    if request.user.is_authenticated and request.user.username != 'invitado':   #Este if no es necesario
        user = request.user #guarda el usuario
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
    if request.method=="POST" and request.user.username != 'invitado':
        if request.POST.get("tachar"):
            vari[0] = ['-','-','-','-']
            vari[1] = ['-','-','-','-']
            vari[2] = ['-','-','-','-']
            vari[3] = ['-','-','-','-']
            vari[4] = ['-','-','-','-']
            vari[5] = ['-','-','-','-']
            vari[6] = ['-','-','-','-']
        else:
            for i in range(7):
                vari[i]=[request.POST.get(etiquetas[i][0],''),request.POST.get(etiquetas[i][1],''),request.POST.get(etiquetas[i][2],''),request.POST.get(etiquetas[i][3],'')]
        
        ops = request.POST.get('opciones','')
        
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

        except Comensal.DoesNotExist:
            answer = Comensal(user=user,opciones=ops,L=L,M=M,X=X,J=J,V=V,S=S,D=S)

        answer.save() #guarda la nueva respuesta en la base de datos

    numdias = ["","","","","","",""]
    today = date.today()
    for i in range (7):
        num = today + timedelta(days=i)
        num = num.strftime('%d/%m/%Y')
        numdias[i] = str(num)
    num_day = today.weekday()
    dias = ["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"]
    j = 0
    for i in range(num_day,7,1):
        dias[i] = dias[i] + " (" + numdias[j] + ")"
        j = j + 1
    for i in range(0,num_day,1):
        dias[i] = dias[i] + " (" + numdias[j] + ")"
        j = j + 1
#    num = [0, 1, 2, 3, 4, 5, 6]
#    dias = {'0':"Lunes", '1':"Martes", '2':"Miercoles", '3':"Jueves", '4':"Viernes", '5':"Sábado", '6':"Domingo"}
    variables = [[],[],[],[],[],[],[]]
    for i in range(7):
        variables[i] = [vari[i], dias[i], etiquetas[i]]

    return render(request, 'blog/parte.html', {'variables': variables, 'title': 'Parte', 'opciones': ops})

#FUNCIÓN PARA MODIFICAR EL PARTE DE CUALQUIER USUARIO (SOLO DISPONIBLE PARA EL ADMINISTRADOR)
@login_required 
def Modificar(request):
    if request.user.username == 'parteadmin':
        mostrar = False
        usernames = User.objects.all()
        names = []
        for uname in usernames:
            names.append(uname.username)

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
        ops = ''
        if request.method=="POST": 
            mostrar = True
            if request.POST.get("mostrar"):
                user = request.POST.get('selectuser','')
                try:    #Para obtener la respuesta anterior si la hay
                    answer = Comensal.objects.get(user=User.objects.get(username=user))    #query para sacar la respuesta anterior
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
            else: #elif request.POST.get("guardar"):
                user = request.POST.get('selectuser','')
                if request.POST.get("tachar"):
                    vari[0] = ['-','-','-','-']
                    vari[1] = ['-','-','-','-']
                    vari[2] = ['-','-','-','-']
                    vari[3] = ['-','-','-','-']
                    vari[4] = ['-','-','-','-']
                    vari[5] = ['-','-','-','-']
                    vari[6] = ['-','-','-','-']
                else:
                    for i in range(7):
                        vari[i]=[request.POST.get(etiquetas[i][0],''),request.POST.get(etiquetas[i][1],''),request.POST.get(etiquetas[i][2],''),request.POST.get(etiquetas[i][3],'')]
                
                ops = request.POST.get('opciones','')
                
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
                    answer = Comensal.objects.get(user=User.objects.get(username=user))    #query para sacar la respuesta anterior
                    answer.opciones = ops
                    answer.L = L
                    answer.M = M
                    answer.X = X
                    answer.J = J
                    answer.V = V
                    answer.S = S
                    answer.D = D

                except Comensal.DoesNotExist:
                    answer = Comensal(user=User.objects.get(username=user),opciones=ops,L=L,M=M,X=X,J=J,V=V,S=S,D=S)

                answer.save() #guarda la nueva respuesta en la base de datos
        else:
            mostrar = False             

        numdias = ["","","","","","",""]
        today = date.today()
        for i in range (7):
            num = today + timedelta(days=i)
            num = num.strftime('%d/%m/%Y')
            numdias[i] = str(num)
        num_day = today.weekday()
        dias = ["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"]
        j = 0
        for i in range(num_day,7,1):
            dias[i] = dias[i] + " (" + numdias[j] + ")"
            j = j + 1
        for i in range(0,num_day,1):
            dias[i] = dias[i] + " (" + numdias[j] + ")"
            j = j + 1
        variables = [[],[],[],[],[],[],[]]
        for i in range(7):
            variables[i] = [vari[i], dias[i], etiquetas[i]]
        return render(request, 'blog/modificar.html', {'variables': variables, 'title': 'Modificar', 'opciones': ops, 'names': names, 'mostrar': mostrar, 'currentuser': user})
    else:
        return render(request, 'blog/inicio.html', {'title': 'Inicio'})

def Inicio(request):
    context = {
        'users': User.objects.all()
    }
    return render(request, 'blog/inicio3.html', context)

@login_required 
def Enlaces(request):
    return render(request, 'blog/enlaces.html', {'title': 'Enlaces'})

#MAIL DE DEPORTE
@login_required 
def Extras(request):
    #current_user = request.user.username
    if  request.user.username == 'parteadmin':
        #Para la fecha en el correo
        numdias = ["","","","","","",""]
        today = date.today()
        for i in range (7):
            num = today + timedelta(days=i)
            num = num.strftime('%d/%m/%Y')
            numdias[i] = str(num)
        num_day = today.weekday()
        dias = ["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"]
        j = 0
        for i in range(num_day,7,1):
            dias[i] = dias[i] + " (" + numdias[j] + ")"
            j = j + 1
        for i in range(0,num_day,1):
            dias[i] = dias[i] + " (" + numdias[j] + ")"
            j = j + 1

        try:
            diad = VariablesGlobales.objects.get()
        except VariablesGlobales.DoesNotExist:
            diad = VariablesGlobales(diadxt=6)
            diad.save()
        num = diad.diadxt
        days = ['Lunes','Martes','Miércoles','Jueves','Viernes','Sábado','Domingo']
        if request.method=="POST": 
            if request.POST.get("correo"):
                usuarios = User.objects.all()
                for usuario in usuarios:
                    destinatario = usuario.email
                    try:    #Para obtener la respuesta si la hay
                        answer = Deportista.objects.get(user=usuario).dxt
                        if answer == 'S':
                            answer = 'SI haces deporte.'
                        else:
                            answer = 'NO haces deporte.'
                        subject = 'Correo semanal de DxT'
                        context =  {'answer': answer}
                        html_message = render_to_string('blog/maildxt.html', {'context': context, 'diacorreo': dias[num]})
                        plain_message = strip_tags(html_message)
                        #from_email = 'From <partebcn@gmail.com>'
                        from_email = EMAIL_HOST_USER
                        to = destinatario
                        mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
                        #html = """<html>
                        #            <body>
                        #                    <h4>¡Buenos días!</h4>
                        #                    <h4></h4>
                        #                    <h4>Esta semana </h4><h3>""" + answer + """</h3><br>
                        #                    <h4>¿Quieres enviar otra respuesta? Entra en el siguiente enlace: https://partebarcelona.pythonanywhere.com/deporte/</h4>
                        #                    <h4>No contestar a este correo, se ha generado automáticamente.</h4>
                        #                    <h4>Atentamente,</h4>
                        #                    <h4></h4>
                        #                    <h4>ParteProgrammingTeam</h4>
                        #            </body>
                        #            </html> """
                        """
                        mensaje = strip_tags(html)
                        send_mail('Correo semanal de Deporte',
                        mensaje,
                        EMAIL_HOST_USER,
                        [destinatario],
                        fail_silently=False)
                        """
                    except Deportista.DoesNotExist:
                        answer = 'N'

            elif request.POST.get("dianuevo"):
                newday = request.POST.get('selectday','')
                num = days.index(newday)
                diad.diadxt = num
        
        diad.save()
        currentday = days[num]
        return render(request, 'blog/extras.html', {'title': 'Extras', 'days': days, 'currentday': currentday})
    else:
        return render(request, 'blog/inicio.html', {'title': 'Inicio'})



#def Deporte(request):
#    return render(request, 'blog/deporte.html', {'title': 'Deporte'})

@login_required 
def deportista(request):
    user = None

    numdias = ["","","","","","",""]
    today = date.today()
    for i in range (7):
        num = today + timedelta(days=i)
        num = num.strftime('%d/%m/%Y')
        numdias[i] = str(num)
    num_day = today.weekday()
    dias = ["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"]
    j = 0
    for i in range(num_day,7,1):
        dias[i] = dias[i] + " (" + numdias[j] + ")"
        j = j + 1
    for i in range(0,num_day,1):
        dias[i] = dias[i] + " (" + numdias[j] + ")"
        j = j + 1

    if request.user.is_authenticated and request.user.username != 'invitado':   #Este if no es necesario
        #user = request.user.username #guarda el nombre de usuario
        user = request.user
    try:    #Para obtener la respuesta anterior si la hay
        answer = Deportista.objects.get(user=user)    #query para sacar la respuesta anterior
        dxt=answer.dxt
        tipo=answer.tipo
    except Deportista.DoesNotExist:
        dxt='O'
        tipo='O'
    #Si se ha enviado una respuesta nueva:
    if request.method=="POST" and request.user.username != 'invitado':  
        observaciones = request.POST.get('observaciones', '')
        dxt = request.POST.get('respuesta','')
        tipo = request.POST.get('tipo','')
        #Si por algun motivo hubiera dos respuestas de un mismo usuario seguramente petaria
        try:
            answer = Deportista.objects.get(user=user)    #query para sacar la respuesta anterior
            answer.observaciones=observaciones
            answer.dxt=dxt
            answer.tipo=tipo
        except Deportista.DoesNotExist:
            answer = Deportista(user=user, observaciones=observaciones, dxt=dxt, tipo=tipo)
        answer.save() #guarda la nueva respuesta en la base de datos
    try:
        diad = VariablesGlobales.objects.get()
        diadxt = diad.diadxt
    except VariablesGlobales.DoesNotExist:
        diadxt = 6
    return render(request, 'blog/deporte.html', {'dxt': dxt, 'title': 'Deporte', 'dia': dias[diadxt], 'tipo': tipo})

@login_required
def Animation(request):
    return render(request, 'blog/animation.html', {'title': 'Animation'})

@login_required
def Encuadernadora(request):
    user = None
    tapa1 = 0
    if request.user.is_authenticated and request.user.username != 'invitado':
        user = request.user
    try:    #Para obtener la respuesta anterior si la hay
        precios = VariablesGlobales.objects.get()
        precio_e6 = precios.precio_e6
        precio_e10 = precios.precio_e10
        precio_e14 = precios.precio_e14
        precio_e20 = precios.precio_e20
        precio_tapa = precios.precio_tapa
        answer = Impresor.objects.get(user=user)    #query para sacar la respuesta anterior
        saldo = answer.saldo
        e6 = answer.e6
        e10 = answer.e10
        e14 = answer.e14
        e20 = answer.e20
        tapas = answer.tapas
    except Impresor.DoesNotExist:
        saldo = 0
        texto_blanco = 0
        texto_color = 0
        imagen_blanco = 0
        imagen_color = 0
        denso_blanco = 0
        denso_color = 0
        e6 = 0
        e10 = 0
        e14 = 0
        e20 = 0
        tapas = 0
    
    #Si se ha enviado una respuesta nueva:
    if request.method=="POST" and request.user.username != 'invitado':  
        e6 = request.POST.get('e6')
        if e6 == '':
            e6 = 0
        e6 = int(e6)
        e10 = request.POST.get('e10')
        if e10 == '':
            e10 = 0
        e10 = int(e10)
        e14 = request.POST.get('e14')
        if e14 == '':
            e14 = 0
        e14 = int(e14)
        e20 = request.POST.get('e20')
        if e20 == '':
            e20 = 0
        e20 = int(e20)

        tapa = request.POST.get('tapa','')
        if (tapa == 'S'):
            tapa1 = 1

        try:
            answer = Impresor.objects.get(user=user)    #query para sacar la respuesta anterior
            saldo = answer.saldo - precio_e6*e6 - precio_e10*e10 - precio_e14*e14 \
            - precio_e20*e20 - precio_tapa*tapa1
            answer.saldo = saldo
            e6 = answer.e6 + abs(e6)
            e10 = answer.e10 + abs(e10)
            e14 = answer.e14 + abs(e14)
            e20 = answer.e20 + abs(e20)
            tapa1 = answer.tapas + abs(tapa1)
            answer.e6 = e6
            answer.e10 = e10
            answer.e14 = e14
            answer.e20 = e20
            answer.tapas = tapa1
        except Impresor.DoesNotExist:
            answer = Impresor(user=user, saldo=saldo, texto_blanco = texto_blanco, texto_color = texto_color, imagen_blanco = imagen_blanco,
            imagen_color = imagen_color, denso_blanco = denso_blanco, denso_color = denso_color, e6=e6, e10=e10, e14=e14, e20=e20, tapas=tapas)
        answer.save() #guarda la nueva respuesta en la base de datos

    return render(request, 'blog/encuadernadora.html', {'title': 'Encuadernadora', 'precio_e6': precio_e6, 'precio_e10': precio_e10, 'precio_e14': precio_e14,
     'precio_e20': precio_e20, 'e6': e6, 'e10': e10, 'e14': e14, 'e20': e20, 'tapas': tapa1, 'precio_tapa': precio_tapa, 'saldo': saldo})

@login_required 
def Impresora(request):
    user = None
    total_blanco = 0
    total_color = 0 
    if request.user.is_authenticated and request.user.username != 'invitado':
        user = request.user
    try:    #Para obtener la respuesta anterior si la hay
        precios = VariablesGlobales.objects.get()
        precio_tblanco = precios.precio_tblanco
        precio_tcolor = precios.precio_tcolor
        precio_iblanco = precios.precio_iblanco
        precio_icolor = precios.precio_icolor
        precio_dblanco = precios.precio_dblanco
        precio_dcolor = precios.precio_dcolor
        answer = Impresor.objects.get(user=user)    #query para sacar la respuesta anterior
        saldo = answer.saldo
        texto_blanco = answer.texto_blanco
        texto_color = answer.texto_color
        imagen_blanco = answer.imagen_blanco
        imagen_color = answer.imagen_color
        denso_blanco = answer.denso_blanco
        denso_color = answer.denso_color
    except Impresor.DoesNotExist:
        saldo = 0
        texto_blanco = 0
        texto_color = 0
        imagen_blanco = 0
        imagen_color = 0
        denso_blanco = 0
        denso_color = 0
        e6 = 0
        e10 = 0
        e14 = 0
        e20 = 0
        tapas = 0

    #Si se ha enviado una respuesta nueva:
    if request.method=="POST" and request.user.username != 'invitado':  
        texto_blanco = request.POST.get('tblanco1')
        if texto_blanco == '':
            texto_blanco = 0
        texto_blanco = int(texto_blanco)
        texto_color = request.POST.get('tcolor1')
        if texto_color == '':
            texto_color = 0
        texto_color = int(texto_color)
        imagen_blanco = request.POST.get('iblanco1')
        if imagen_blanco == '':
            imagen_blanco = 0
        imagen_blanco = int(imagen_blanco)
        imagen_color = request.POST.get('icolor1')
        if imagen_color == '':
            imagen_color = 0
        imagen_color = int(imagen_color)
        denso_blanco = request.POST.get('dblanco1')
        if denso_blanco == '':
            denso_blanco = 0
        denso_blanco = int(denso_blanco)
        denso_color = request.POST.get('dcolor1')
        if denso_color == '':
            denso_color = 0
        denso_color = int(denso_color)

        try:
            answer = Impresor.objects.get(user=user)    #query para sacar la respuesta anterior
            saldo = answer.saldo - precio_tblanco*texto_blanco - precio_iblanco*imagen_blanco - precio_dblanco*denso_blanco \
            - precio_tcolor*texto_color - precio_icolor*imagen_color - precio_dcolor*denso_color
            answer.saldo = saldo
            texto_blanco = answer.texto_blanco + abs(texto_blanco)
            texto_color = answer.texto_color + abs(texto_color)
            imagen_blanco = answer.imagen_blanco + abs(imagen_blanco)
            imagen_color = answer.imagen_color + abs(imagen_color)
            denso_blanco = answer.denso_blanco + abs(denso_blanco)
            denso_color = answer.denso_color + abs(denso_color)
            answer.texto_blanco = texto_blanco
            answer.texto_color = texto_color
            answer.imagen_blanco = imagen_blanco
            answer.imagen_color = imagen_color
            answer.denso_blanco = denso_blanco
            answer.denso_color = denso_color
        except Impresor.DoesNotExist:
            answer = Impresor(user=user, saldo=saldo, texto_blanco = texto_blanco, texto_color = texto_color, imagen_blanco = imagen_blanco,
            imagen_color = imagen_color, denso_blanco = denso_blanco, denso_color = denso_color, e6=e6, e10=e10, e14=e14, e20=e20, tapas=tapas)
        answer.save() #guarda la nueva respuesta en la base de datos
        total_blanco = texto_blanco*precio_tblanco + imagen_blanco*precio_iblanco + denso_blanco*precio_dblanco
        total_color = texto_color*precio_tcolor + imagen_color*precio_icolor + denso_color*precio_dcolor 
    return render(request, 'blog/impresora.html', {'title': 'Impresora', 'tblanco': texto_blanco, 'tcolor': texto_color, 'iblanco': imagen_blanco,
    'icolor': imagen_color, 'dblanco': denso_blanco, 'dcolor': denso_color, 'saldo': saldo, 'totblanco': total_blanco, 'totcolor': total_color,
    'ptb': precio_tblanco, 'ptc': precio_tcolor, 'pib': precio_iblanco, 'pic': precio_icolor, 'pdb': precio_dblanco, 'pdc': precio_dcolor})


@login_required
def parte_to_pdf(request):
    template_name = 'blog/tex/test.tex'
    today = date.today()
    dias = ["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"]
    meses = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
    try:
        diap = VariablesGlobales.objects.get()
    except VariablesGlobales.DoesNotExist:
        diap = VariablesGlobales(diadxt=6,diaparte=6)
        diap.save()
    num_day = diap.diaparte
    diferencia = num_day-today.weekday()
    if diferencia < 0:
        diferencia = 7 + diferencia
    today = today + timedelta(days=diferencia)
    #num_day = today.weekday()
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
        'Fiambrera': 0,
        'Bocadillo-Ans': 0,
        'BocadilloPeq-Ans': 0
    }
    mediamañana = {
        '-': 0,
        'Si': 0
    }
    bocayfiambreras = {     #ESTO ES DE LA COMDIA DEL DIA SIGUIENTE
        'Bocadillo-Pequeño': 0,
        'Bocadillo': 0,
        'Fiambrera': 0,
        'Bocadillo-Ans': 0,
        'BocadilloPeq-Ans': 0
    }
    usuariosBocyF = {       #ESTO ES DE LA COMIDA DEL DIA SIGUIENTE
        'Bocadillo-Pequeño': [],
        'Bocadillo': [],
        'Fiambrera': [],
        'Bocadillo-Ans': [],
        'BocadilloPeq-Ans': []
    }
    #DIETA
    usuariosDietaB = []
    usuariosDietaL = []
    usuariosDietaD = []
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
        'Fiambrera': 0,
        'Bocadillo-Ans': 0,
        'BocadilloPeq-Ans': 0
    }
    mediamañanaD = {
        '-': 0,
        'Si': 0
    }
    bocayfiambrerasD = {
        'Bocadillo-Pequeño': 0,
        'Bocadillo': 0,
        'Fiambrera': 0,
        'Bocadillo-Ans': 0,
        'BocadilloPeq-Ans': 0
    }
    usuariosBocyFD = {
        'Bocadillo-Pequeño': [],
        'Bocadillo': [],
        'Fiambrera': [],
        'Bocadillo-Ans': [],
        'BocadilloPeq-Ans': [],
        'BocCenaPeq': [],
        'BocCena': []
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
        'Fiambrera': 0,
        'Bocadillo-Ans': 0,
        'BocadilloPeq-Ans': 0
    }
    mediamañanaE = {
        '-': 0,
        'Si': 0
    }
    bocayfiambrerasE = {
        'Bocadillo-Pequeño': 0,
        'Bocadillo': 0,
        'Fiambrera': 0,
        'Bocadillo-Ans': 0,
        'BocadilloPeq-Ans': 0
    }
    usuariosBocyFE = {
        'Bocadillo-Pequeño': [],
        'Bocadillo': [],
        'Fiambrera': [],
        'Bocadillo-Ans': [],
        'BocadilloPeq-Ans': []
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
        'Fiambrera': 0,
        'Bocadillo-Ans': 0,
        'BocadilloPeq-Ans': 0
    }
    mediamañanaB = {
        '-': 0,
        'Si': 0
    }
    bocayfiambrerasB = {
        'Bocadillo-Pequeño': 0,
        'Bocadillo': 0,
        'Fiambrera': 0,
        'Bocadillo-Ans': 0,
        'BocadilloPeq-Ans': 0
    }
    usuariosBocyFB = {
        'Bocadillo-Pequeño': [],
        'Bocadillo': [],
        'Fiambrera': [],
        'Bocadillo-Ans': [],
        'BocadilloPeq-Ans': []
    }

    #Para obtener la respuesta anterior si la hay
    #comensales = Comensal.objects.get()    #query para sacar las respuestas

    #for comensal in comensales.user:

    for com in Comensal.objects.all():
        try:
            comensal1 = com.user    #Usuario
            comensal = comensal1.username   #Nombre
            parte = Comensal.objects.get(user=comensal1)
            if parte.opciones == 'Normal':
                if num_day == 0:
                    comida[parte.L.l]+=1
                    cena[parte.L.d]+=1
                    desayuno[parte.M.b]+=1
                    mediamañana[parte.M.m]+=1
                    if (parte.M.l == 'Fiambrera') or (parte.M.l == 'Bocadillo-Pequeño') or (parte.M.l == 'Bocadillo'):
                        bocayfiambreras[parte.M.l]+=1
                        usuariosBocyF[parte.M.l].append(comensal)
                    if (parte.M.d == 'Bocadillo-Ans') or (parte.M.d == 'BocadilloPeq-Ans'):
                        bocayfiambreras[parte.M.d]+=1
                        usuariosBocyF[parte.M.d].append(comensal)
                elif num_day == 1:
                    comida[parte.M.l]+=1
                    cena[parte.M.d]+=1
                    desayuno[parte.X.b]+=1
                    mediamañana[parte.X.m]+=1
                    if (parte.X.l == 'Fiambrera') or (parte.X.l == 'Bocadillo-Pequeño') or (parte.X.l == 'Bocadillo'):
                        bocayfiambreras[parte.X.l]+=1
                        usuariosBocyF[parte.X.l].append(comensal)
                    if (parte.X.d == 'Bocadillo-Ans') or (parte.X.d == 'BocadilloPeq-Ans'):
                        bocayfiambreras[parte.X.d]+=1
                        usuariosBocyF[parte.X.d].append(comensal)
                elif num_day == 2:
                    comida[parte.X.l]+=1
                    cena[parte.X.d]+=1
                    desayuno[parte.J.b]+=1
                    mediamañana[parte.J.m]+=1
                    if (parte.J.l == 'Fiambrera') or (parte.J.l == 'Bocadillo-Pequeño') or (parte.J.l == 'Bocadillo'):
                        bocayfiambreras[parte.J.l]+=1
                        usuariosBocyF[parte.J.l].append(comensal)
                    if (parte.J.d == 'Bocadillo-Ans') or (parte.J.d == 'BocadilloPeq-Ans'):
                        bocayfiambreras[parte.J.d]+=1
                        usuariosBocyF[parte.J.d].append(comensal)
                elif num_day == 3:
                    comida[parte.J.l]+=1
                    cena[parte.J.d]+=1
                    desayuno[parte.V.b]+=1
                    mediamañana[parte.V.m]+=1
                    if (parte.V.l == 'Fiambrera') or (parte.V.l == 'Bocadillo-Pequeño') or (parte.V.l == 'Bocadillo'):
                        bocayfiambreras[parte.V.l]+=1
                        usuariosBocyF[parte.V.l].append(comensal)
                    if (parte.V.d == 'Bocadillo-Ans') or (parte.V.d == 'BocadilloPeq-Ans'):
                        bocayfiambreras[parte.V.d]+=1
                        usuariosBocyF[parte.V.d].append(comensal)
                elif num_day == 4:
                    comida[parte.V.l]+=1
                    cena[parte.V.d]+=1
                    desayuno[parte.S.b]+=1
                    mediamañana[parte.S.m]+=1
                    if (parte.S.l == 'Fiambrera') or (parte.S.l == 'Bocadillo-Pequeño') or (parte.S.l == 'Bocadillo'):
                        bocayfiambreras[parte.S.l]+=1
                        usuariosBocyF[parte.S.l].append(comensal)
                    if (parte.S.d == 'Bocadillo-Ans') or (parte.S.d == 'BocadilloPeq-Ans'):
                        bocayfiambreras[parte.S.d]+=1
                        usuariosBocyF[parte.S.d].append(comensal)
                elif num_day == 5:
                    comida[parte.S.l]+=1
                    cena[parte.S.d]+=1
                    desayuno[parte.D.b]+=1
                    mediamañana[parte.D.m]+=1
                    if (parte.D.l == 'Fiambrera') or (parte.D.l == 'Bocadillo-Pequeño') or (parte.D.l == 'Bocadillo'):
                        bocayfiambreras[parte.D.l]+=1
                        usuariosBocyF[parte.D.l].append(comensal)
                    if (parte.D.d == 'Bocadillo-Ans') or (parte.D.d == 'BocadilloPeq-Ans'):
                        bocayfiambreras[parte.D.d]+=1
                        usuariosBocyF[parte.D.d].append(comensal)
                elif num_day == 6:
                    comida[parte.D.l]+=1
                    cena[parte.D.d]+=1
                    desayuno[parte.L.b]+=1
                    mediamañana[parte.L.m]+=1
                    if (parte.L.l == 'Fiambrera') or (parte.L.l == 'Bocadillo-Pequeño') or (parte.L.l == 'Bocadillo'):
                        bocayfiambreras[parte.L.l]+=1
                        usuariosBocyF[parte.L.l].append(comensal)
                    if (parte.L.d == 'Bocadillo-Ans') or (parte.L.d == 'BocadilloPeq-Ans'):
                        bocayfiambreras[parte.L.d]+=1
                        usuariosBocyF[parte.L.d].append(comensal)

            elif parte.opciones == 'Dieta':
                tipo['dieta']+=1
                #usuariosDieta.append(comensal)
                if num_day == 0:
                    comidaD[parte.L.l]+=1
                    cenaD[parte.L.d]+=1
                    desayunoD[parte.M.b]+=1
                    mediamañanaD[parte.M.m]+=1
                    if (parte.M.l == 'Fiambrera') or (parte.M.l == 'Bocadillo-Pequeño') or (parte.M.l == 'Bocadillo'):
                        bocayfiambrerasD[parte.M.l]+=1
                        usuariosBocyFD[parte.M.l].append(comensal)
                    if (parte.M.d == 'Bocadillo-Ans') or (parte.M.d == 'BocadilloPeq-Ans'):
                        bocayfiambrerasD[parte.M.d]+=1
                        usuariosBocyFD[parte.M.d].append(comensal)
                    if (parte.L.l == 'Normal'):
                        usuariosDietaL.append(comensal)
                    if (parte.L.d == 'Normal'):
                        usuariosDietaD.append(comensal)
                    elif (parte.L.d == 'Bocadillo-Pequeño'):
                        usuariosBocyFD['BocCenaPeq'].append(comensal)
                    elif (parte.L.d == 'Bocadillo'):
                        usuariosBocyFD['BocCena'].append(comensal)
                    if (parte.M.b == 'Normal'):
                        usuariosDietaB.append(comensal)
                elif num_day == 1:
                    comidaD[parte.M.l]+=1
                    cenaD[parte.M.d]+=1
                    desayunoD[parte.X.b]+=1
                    mediamañanaD[parte.X.m]+=1
                    if (parte.X.l == 'Fiambrera') or (parte.X.l == 'Bocadillo-Pequeño') or (parte.X.l == 'Bocadillo'):
                        bocayfiambrerasD[parte.X.l]+=1
                        usuariosBocyFD[parte.X.l].append(comensal)
                    if (parte.X.d == 'Bocadillo-Ans') or (parte.X.d == 'BocadilloPeq-Ans'):
                        bocayfiambrerasD[parte.X.d]+=1
                        usuariosBocyFD[parte.X.d].append(comensal)
                    if (parte.M.l == 'Normal'):
                        usuariosDietaL.append(comensal)
                    if (parte.M.d == 'Normal'):
                        usuariosDietaD.append(comensal)
                    elif (parte.M.d == 'Bocadillo-Pequeño'):
                        usuariosBocyFD['BocCenaPeq'].append(comensal)
                    elif (parte.M.d == 'Bocadillo'):
                        usuariosBocyFD['BocCena'].append(comensal)
                    if (parte.X.b == 'Normal'):
                        usuariosDietaB.append(comensal)
                elif num_day == 2:
                    comidaD[parte.X.l]+=1
                    cenaD[parte.X.d]+=1
                    desayunoD[parte.J.b]+=1
                    mediamañanaD[parte.J.m]+=1
                    if (parte.J.l == 'Fiambrera') or (parte.J.l == 'Bocadillo-Pequeño') or (parte.J.l == 'Bocadillo'):
                        bocayfiambrerasD[parte.J.l]+=1
                        usuariosBocyFD[parte.J.l].append(comensal)
                    if (parte.J.d == 'Bocadillo-Ans') or (parte.J.d == 'BocadilloPeq-Ans'):
                        bocayfiambrerasD[parte.J.d]+=1
                        usuariosBocyFD[parte.J.d].append(comensal)
                    if (parte.X.l == 'Normal'):
                        usuariosDietaL.append(comensal)
                    if (parte.X.d == 'Normal'):
                        usuariosDietaD.append(comensal)
                    elif (parte.X.d == 'Bocadillo-Pequeño'):
                        usuariosBocyFD['BocCenaPeq'].append(comensal)
                    elif (parte.X.d == 'Bocadillo'):
                        usuariosBocyFD['BocCena'].append(comensal)
                    if (parte.J.b == 'Normal'):
                        usuariosDietaB.append(comensal)
                elif num_day == 3:
                    comidaD[parte.J.l]+=1
                    cenaD[parte.J.d]+=1
                    desayunoD[parte.V.b]+=1
                    mediamañanaD[parte.V.m]+=1
                    if (parte.V.l == 'Fiambrera') or (parte.V.l == 'Bocadillo-Pequeño') or (parte.V.l == 'Bocadillo'):
                        bocayfiambrerasD[parte.V.l]+=1
                        usuariosBocyFD[parte.V.l].append(comensal)
                    if (parte.V.d == 'Bocadillo-Ans') or (parte.V.d == 'BocadilloPeq-Ans'):
                        bocayfiambrerasD[parte.V.d]+=1
                        usuariosBocyFD[parte.V.d].append(comensal)
                    if (parte.J.l == 'Normal'):
                        usuariosDietaL.append(comensal)
                    if (parte.J.d == 'Normal'):
                        usuariosDietaD.append(comensal)
                    elif (parte.J.d == 'Bocadillo-Pequeño'):
                        usuariosBocyFD['BocCenaPeq'].append(comensal)
                    elif (parte.J.d == 'Bocadillo'):
                        usuariosBocyFD['BocCena'].append(comensal)
                    if (parte.V.b == 'Normal'):
                        usuariosDietaB.append(comensal)
                elif num_day == 4:
                    comidaD[parte.V.l]+=1
                    cenaD[parte.V.d]+=1
                    desayunoD[parte.S.b]+=1
                    mediamañanaD[parte.S.m]+=1
                    if (parte.S.l == 'Fiambrera') or (parte.S.l == 'Bocadillo-Pequeño') or (parte.S.l == 'Bocadillo'):
                        bocayfiambrerasD[parte.S.l]+=1
                        usuariosBocyFD[parte.S.l].append(comensal)
                    if (parte.S.d == 'Bocadillo-Ans') or (parte.S.d == 'BocadilloPeq-Ans'):
                        bocayfiambrerasD[parte.S.d]+=1
                        usuariosBocyFD[parte.S.d].append(comensal)
                    if (parte.V.l == 'Normal'):
                        usuariosDietaL.append(comensal)
                    if (parte.V.d == 'Normal'):
                        usuariosDietaD.append(comensal)
                    elif (parte.V.d == 'Bocadillo-Pequeño'):
                        usuariosBocyFD['BocCenaPeq'].append(comensal)
                    elif (parte.V.d == 'Bocadillo'):
                        usuariosBocyFD['BocCena'].append(comensal)
                    if (parte.S.b == 'Normal'):
                        usuariosDietaB.append(comensal)
                elif num_day == 5:
                    comidaD[parte.S.l]+=1
                    cenaD[parte.S.d]+=1
                    desayunoD[parte.D.b]+=1
                    mediamañanaD[parte.D.m]+=1
                    if (parte.D.l == 'Fiambrera') or (parte.D.l == 'Bocadillo-Pequeño') or (parte.D.l == 'Bocadillo'):
                        bocayfiambrerasD[parte.D.l]+=1
                        usuariosBocyFD[parte.D.l].append(comensal)
                    if (parte.D.d == 'Bocadillo-Ans') or (parte.D.d == 'BocadilloPeq-Ans'):
                        bocayfiambrerasD[parte.D.d]+=1
                        usuariosBocyFD[parte.D.d].append(comensal)
                    if (parte.S.l == 'Normal'):
                        usuariosDietaL.append(comensal)
                    if (parte.S.d == 'Normal'):
                        usuariosDietaD.append(comensal)
                    elif (parte.S.d == 'Bocadillo-Pequeño'):
                        usuariosBocyFD['BocCenaPeq'].append(comensal)
                    elif (parte.S.d == 'Bocadillo'):
                        usuariosBocyFD['BocCena'].append(comensal)
                    if (parte.D.b == 'Normal'):
                        usuariosDietaB.append(comensal)
                elif num_day == 6:
                    comidaD[parte.D.l]+=1
                    cenaD[parte.D.d]+=1
                    desayunoD[parte.L.b]+=1
                    mediamañanaD[parte.L.m]+=1
                    if (parte.L.l == 'Fiambrera') or (parte.L.l == 'Bocadillo-Pequeño') or (parte.L.l == 'Bocadillo'):
                        bocayfiambrerasD[parte.L.l]+=1
                        usuariosBocyFD[parte.L.l].append(comensal)
                    if (parte.L.d == 'Bocadillo-Ans') or (parte.L.d == 'BocadilloPeq-Ans'):
                        bocayfiambrerasD[parte.L.d]+=1
                        usuariosBocyFD[parte.L.d].append(comensal)
                    if (parte.D.l == 'Normal'):
                        usuariosDietaL.append(comensal)
                    if (parte.D.d == 'Normal'):
                        usuariosDietaD.append(comensal)
                    elif (parte.D.d == 'Bocadillo-Pequeño'):
                        usuariosBocyFD['BocCenaPeq'].append(comensal)
                    elif (parte.D.d == 'Bocadillo'):
                        usuariosBocyFD['BocCena'].append(comensal)
                    if (parte.L.b == 'Normal'):
                        usuariosDietaB.append(comensal)
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
                    if (parte.M.d == 'Bocadillo-Ans') or (parte.M.d == 'BocadilloPeq-Ans'):
                        bocayfiambrerasE[parte.M.d]+=1
                        usuariosBocyFE[parte.M.d].append(comensal)
                elif num_day == 1:
                    comidaE[parte.M.l]+=1
                    cenaE[parte.M.d]+=1
                    desayunoE[parte.X.b]+=1
                    mediamañanaE[parte.X.m]+=1
                    if (parte.X.l == 'Fiambrera') or (parte.X.l == 'Bocadillo-Pequeño') or (parte.X.l == 'Bocadillo'):
                        bocayfiambrerasE[parte.X.l]+=1
                        usuariosBocyFE[parte.X.l].append(comensal)
                    if (parte.X.d == 'Bocadillo-Ans') or (parte.X.d == 'BocadilloPeq-Ans'):
                        bocayfiambrerasE[parte.X.d]+=1
                        usuariosBocyFE[parte.X.d].append(comensal)
                elif num_day == 2:
                    comidaE[parte.X.l]+=1
                    cenaE[parte.X.d]+=1
                    desayunoE[parte.J.b]+=1
                    mediamañanaE[parte.J.m]+=1
                    if (parte.J.l == 'Fiambrera') or (parte.J.l == 'Bocadillo-Pequeño') or (parte.J.l == 'Bocadillo'):
                        bocayfiambrerasE[parte.J.l]+=1
                        usuariosBocyFE[parte.J.l].append(comensal)
                    if (parte.J.d == 'Bocadillo-Ans') or (parte.J.d == 'BocadilloPeq-Ans'):
                        bocayfiambrerasE[parte.J.d]+=1
                        usuariosBocyFE[parte.J.d].append(comensal)
                elif num_day == 3:
                    comidaE[parte.J.l]+=1
                    cenaE[parte.J.d]+=1
                    desayunoE[parte.V.b]+=1
                    mediamañanaE[parte.V.m]+=1
                    if (parte.V.l == 'Fiambrera') or (parte.V.l == 'Bocadillo-Pequeño') or (parte.V.l == 'Bocadillo'):
                        bocayfiambrerasE[parte.V.l]+=1
                        usuariosBocyFE[parte.V.l].append(comensal)
                    if (parte.V.d == 'Bocadillo-Ans') or (parte.V.d == 'BocadilloPeq-Ans'):
                        bocayfiambrerasE[parte.V.d]+=1
                        usuariosBocyFE[parte.V.d].append(comensal)
                elif num_day == 4:
                    comidaE[parte.V.l]+=1
                    cenaE[parte.V.d]+=1
                    desayunoE[parte.S.b]+=1
                    mediamañanaE[parte.S.m]+=1
                    if (parte.S.l == 'Fiambrera') or (parte.S.l == 'Bocadillo-Pequeño') or (parte.S.l == 'Bocadillo'):
                        bocayfiambrerasE[parte.S.l]+=1
                        usuariosBocyFE[parte.S.l].append(comensal)
                    if (parte.S.d == 'Bocadillo-Ans') or (parte.S.d == 'BocadilloPeq-Ans'):
                        bocayfiambrerasE[parte.S.d]+=1
                        usuariosBocyFE[parte.S.d].append(comensal)
                elif num_day == 5:
                    comidaE[parte.S.l]+=1
                    cenaE[parte.S.d]+=1
                    desayunoE[parte.D.b]+=1
                    mediamañanaE[parte.D.m]+=1
                    if (parte.D.l == 'Fiambrera') or (parte.D.l == 'Bocadillo-Pequeño') or (parte.D.l == 'Bocadillo'):
                        bocayfiambrerasE[parte.D.l]+=1
                        usuariosBocyFE[parte.D.l].append(comensal)
                    if (parte.D.d == 'Bocadillo-Ans') or (parte.D.d == 'BocadilloPeq-Ans'):
                        bocayfiambrerasE[parte.D.d]+=1
                        usuariosBocyFE[parte.D.d].append(comensal)
                elif num_day == 6:
                    comidaE[parte.D.l]+=1
                    cenaE[parte.D.d]+=1
                    desayunoE[parte.L.b]+=1
                    mediamañanaE[parte.L.m]+=1
                    if (parte.L.l == 'Fiambrera') or (parte.L.l == 'Bocadillo-Pequeño') or (parte.L.l == 'Bocadillo'):
                        bocayfiambrerasE[parte.L.l]+=1
                        usuariosBocyFE[parte.L.l].append(comensal)
                    if (parte.L.d == 'Bocadillo-Ans') or (parte.L.d == 'BocadilloPeq-Ans'):
                        bocayfiambrerasE[parte.L.d]+=1
                        usuariosBocyFE[parte.L.d].append(comensal)
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
                    if (parte.M.d == 'Bocadillo-Ans') or (parte.M.d == 'BocadilloPeq-Ans'):
                        bocayfiambrerasB[parte.M.d]+=1
                        usuariosBocyFB[parte.M.d].append(comensal)
                elif num_day == 1:
                    comidaB[parte.M.l]+=1
                    cenaB[parte.M.d]+=1
                    desayunoB[parte.X.b]+=1
                    mediamañanaB[parte.X.m]+=1
                    if (parte.X.l == 'Fiambrera') or (parte.X.l == 'Bocadillo-Pequeño') or (parte.X.l == 'Bocadillo'):
                        bocayfiambrerasB[parte.X.l]+=1
                        usuariosBocyFB[parte.X.l].append(comensal)
                    if (parte.X.d == 'Bocadillo-Ans') or (parte.X.d == 'BocadilloPeq-Ans'):
                        bocayfiambrerasB[parte.X.d]+=1
                        usuariosBocyFB[parte.X.d].append(comensal)
                elif num_day == 2:
                    comidaB[parte.X.l]+=1
                    cenaB[parte.X.d]+=1
                    desayunoB[parte.J.b]+=1
                    mediamañanaB[parte.J.m]+=1
                    if (parte.J.l == 'Fiambrera') or (parte.J.l == 'Bocadillo-Pequeño') or (parte.J.l == 'Bocadillo'):
                        bocayfiambrerasB[parte.J.l]+=1
                        usuariosBocyFB[parte.J.l].append(comensal)
                    if (parte.J.d == 'Bocadillo-Ans') or (parte.J.d == 'BocadilloPeq-Ans'):
                        bocayfiambrerasB[parte.J.d]+=1
                        usuariosBocyFB[parte.J.d].append(comensal)
                elif num_day == 3:
                    comidaB[parte.J.l]+=1
                    cenaB[parte.J.d]+=1
                    desayunoB[parte.V.b]+=1
                    mediamañanaB[parte.V.m]+=1
                    if (parte.V.l == 'Fiambrera') or (parte.V.l == 'Bocadillo-Pequeño') or (parte.V.l == 'Bocadillo'):
                        bocayfiambrerasB[parte.V.l]+=1
                        usuariosBocyFB[parte.V.l].append(comensal)
                    if (parte.V.d == 'Bocadillo-Ans') or (parte.V.d == 'BocadilloPeq-Ans'):
                        bocayfiambrerasB[parte.V.d]+=1
                        usuariosBocyFB[parte.V.d].append(comensal)
                elif num_day == 4:
                    comidaB[parte.V.l]+=1
                    cenaB[parte.V.d]+=1
                    desayunoB[parte.S.b]+=1
                    mediamañanaB[parte.S.m]+=1
                    if (parte.S.l == 'Fiambrera') or (parte.S.l == 'Bocadillo-Pequeño') or (parte.S.l == 'Bocadillo'):
                        bocayfiambrerasB[parte.S.l]+=1
                        usuariosBocyFB[parte.S.l].append(comensal)
                    if (parte.S.d == 'Bocadillo-Ans') or (parte.S.d == 'BocadilloPeq-Ans'):
                        bocayfiambrerasB[parte.S.d]+=1
                        usuariosBocyFB[parte.S.d].append(comensal)
                elif num_day == 5:
                    comidaB[parte.S.l]+=1
                    cenaB[parte.S.d]+=1
                    desayunoB[parte.D.b]+=1
                    mediamañanaB[parte.D.m]+=1
                    if (parte.D.l == 'Fiambrera') or (parte.D.l == 'Bocadillo-Pequeño') or (parte.D.l == 'Bocadillo'):
                        bocayfiambrerasB[parte.D.l]+=1
                        usuariosBocyFB[parte.D.l].append(comensal)
                    if (parte.D.d == 'Bocadillo-Ans') or (parte.D.d == 'BocadilloPeq-Ans'):
                        bocayfiambrerasB[parte.D.d]+=1
                        usuariosBocyFB[parte.D.d].append(comensal)
                elif num_day == 6:
                    comidaB[parte.D.l]+=1
                    cenaB[parte.D.d]+=1
                    desayunoB[parte.L.b]+=1
                    mediamañanaB[parte.L.m]+=1
                    if (parte.L.l == 'Fiambrera') or (parte.L.l == 'Bocadillo-Pequeño') or (parte.L.l == 'Bocadillo'):
                        bocayfiambrerasB[parte.L.l]+=1
                        usuariosBocyFB[parte.L.l].append(comensal)
                    if (parte.L.d == 'Bocadillo-Ans') or (parte.L.d == 'BocadilloPeq-Ans'):
                        bocayfiambrerasB[parte.L.d]+=1
                        usuariosBocyFB[parte.L.d].append(comensal)
        except Comensal.DoesNotExist:
            a = 1

    #parte = Comensal.objects.get(user='parteadmin')
    #letra = 'L'
    #comida[parte.L.l]+=1
    #observaciones = comida[parte.L.l]


    vector = [comida, cena, desayuno, mediamañana, bocayfiambreras, comidaD, cenaD, desayunoD, mediamañanaD, bocayfiambrerasD, comidaB, cenaB, desayunoB, mediamañanaB, bocayfiambrerasB, comidaE, cenaE, desayunoE, mediamañanaE, bocayfiambrerasE]
    contador1 = 0
    for diccionario in vector:
        keys1 = diccionario.keys()
        for key in keys1:
            if diccionario[key] == 0:
                diccionario[key] = ""
        vector[contador1]=diccionario
        contador1 = contador1 + 1


    observaciones = ''
    if request.method=="POST":
        observaciones = request.POST.get('observaciones', '')
    #context = {'title': 'Parte en PDF', 'tipo': tipo, 'observaciones': observaciones, 'numerodia': today.day, 'mes': meses[today.month-1],
    # 'año': today.year, 'dia':dia,
    # 'comida': comida, 'cena': cena, 'desayuno': desayuno, 'mediamañana': mediamañana, 'bocayfiambreras': bocayfiambreras, 'usuariosBocyF': usuariosBocyF,
    # 'comidaD': comidaD, 'cenaD': cenaD, 'desayunoD': desayunoD, 'mediamañanaD': mediamañanaD, 'bocayfiambrerasD': bocayfiambrerasD, 'usuariosBocyFD': usuariosBocyFD,
    # 'comidaB': comidaB, 'cenaB': cenaB, 'desayunoB': desayunoB, 'mediamañanaB': mediamañanaB, 'bocayfiambrerasB': bocayfiambrerasB, 'usuariosBocyFB': usuariosBocyFB,
    # 'comidaE': comidaE, 'cenaE': cenaE, 'desayunoE': desayunoE, 'mediamañanaE': mediamañanaE, 'bocayfiambrerasE': bocayfiambrerasE, 'usuariosBocyFE': usuariosBocyFE,
    # 'usuariosDietaB': usuariosDietaB, 'usuariosDietaL': usuariosDietaL, 'usuariosDietaD': usuariosDietaD}

    context = {'title': 'Parte en PDF', 'tipo': tipo, 'observaciones': observaciones, 'numerodia': today.day, 'mes': meses[today.month-1],
     'año': today.year, 'dia':dia,
     'comida': vector[0], 'cena': vector[1], 'desayuno': vector[2], 'mediamañana': vector[3], 'bocayfiambreras': vector[4], 'usuariosBocyF': usuariosBocyF,
     'comidaD': vector[5], 'cenaD': vector[6], 'desayunoD': vector[7], 'mediamañanaD': vector[8], 'bocayfiambrerasD': vector[9], 'usuariosBocyFD': usuariosBocyFD,
     'comidaB': vector[10], 'cenaB': vector[11], 'desayunoB': vector[12], 'mediamañanaB': vector[13], 'bocayfiambrerasB': vector[14], 'usuariosBocyFB': usuariosBocyFB,
     'comidaE': vector[15], 'cenaE': vector[16], 'desayunoE': vector[17], 'mediamañanaE': vector[18], 'bocayfiambrerasE': vector[19], 'usuariosBocyFE': usuariosBocyFE,
     'usuariosDietaB': usuariosDietaB, 'usuariosDietaL': usuariosDietaL, 'usuariosDietaD': usuariosDietaD}

    return render_to_pdf(request, template_name, context, filename='PartePDF.pdf')

#        return render_to_pdf(request, template_name, "ERROR!!!",filename='PartePDF.pdf')


@login_required
def parte_to_pdf2(request):
    template_name = 'blog/tex/parte2.tex'
    today = date.today()
    dias = ["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"]
    meses = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
    try:
        diap = VariablesGlobales.objects.get()
    except VariablesGlobales.DoesNotExist:
        diap = VariablesGlobales(diadxt=6,diaparte=6)
        diap.save()
    num_day = diap.diaparte
    diferencia = num_day-today.weekday()
    if diferencia < 0:
        diferencia = 7 + diferencia
    today = today + timedelta(days=diferencia)
    #num_day = today.weekday()
    dia = dias[num_day]
    variables = []
    contadores = { 'Dieta': [0, 0, 0, 0, 0],
                   'Enfermo': [0, 0, 0, 0, 0],
                   'Blando': [0, 0, 0, 0, 0],
                   'Normal': [0, 0, 0, 0, 0]}
    totales = [0, 0, 0, 0, 0]
    blando = False
    enfermo = False


    for com in Comensal.objects.all():
        usuario = com.user.username
        tipo = com.opciones

        if num_day == 0:
            dia1 = com.L
            dia2 = com.M
        elif num_day == 1:
            dia1 = com.M
            dia2 = com.X
        elif num_day == 2:
            dia1 = com.X
            dia2 = com.J
        elif num_day == 3:
            dia1 = com.J
            dia2 = com.V
        elif num_day == 4:
            dia1 = com.V
            dia2 = com.S
        elif num_day == 5:
            dia1 = com.S
            dia2 = com.D
        elif num_day == 6:
            dia1 = com.D
            dia2 = com.L
        #HAY QUE ACTUALIZAR EL DICCIONARIO => ACCEDER A LA CLAVE Y A 1, 2 ... DEPENDE DEL DIA Y COMIDA
        if dia1.l == 'Normal':
            #my_dict = { **my_dict, 'Pooja': 12}
            #contadores = { **contadores, tipo: contadores.get(tipo)[0] + 1}
            contadores[tipo][0] = contadores[tipo][0] + 1
            totales[0] += 1
        if dia1.d == 'Normal':
            contadores[tipo][1] = contadores[tipo][1] + 1
            totales[1] += 1
        if dia2.b == 'Normal':
            contadores[tipo][2] = contadores[tipo][2] + 1
            totales[2] += 1
        if dia2.l == 'Normal':
            contadores[tipo][3] = contadores[tipo][3] + 1
            totales[3] += 1
        if dia2.d == 'Normal':
            contadores[tipo][4] = contadores[tipo][4] + 1
            totales[4] += 1

        if ((dia1.l == '-') and (dia1.d == '-') and (dia2.b == '-') and (dia2.l == '-') and (dia2.d == '-')):
            tipo = 'Normal'
        
        if tipo == 'Enfermo':
            enfermo = True
        elif tipo == 'Blando':
            blando = True
        

        var = [usuario, dia1, dia2, tipo]
        variables.append(var)

    #totales = contadores['Dieta'] + contadores['Enfermo'] + contadores['Blando'] + contadores['Normal']
    context = {'title': 'Parte en PDF', 'variables': variables, 'numerodia': today.day, 'mes': meses[today.month-1],
     'enfermo': enfermo, 'blando': blando, 'contadores': contadores, 'totales': totales,
     'año': today.year, 'dia':dia}

    return render_to_pdf(request, template_name, context, filename='PartePDF2.pdf')

#ADMINISTRADOR DEL PARTE (CONTIENE EL ENVÍO DE CORREOS RECORDATORIO PARTE)
@login_required
def Imprimir(request):
    if request.user.username == 'parteadmin':
        #Fecha variable del parte a imprimir
        try:
            diap = VariablesGlobales.objects.get()
        except VariablesGlobales.DoesNotExist:
            diap = VariablesGlobales(diadxt=6,diaparte=6)
            diap.save()
        num = diap.diaparte
        days = ['Lunes','Martes','Miércoles','Jueves','Viernes','Sábado','Domingo']


        #Correo recordatorio parte
        if request.method=="POST":
            if request.POST.get("correo"):
                usuarios = User.objects.all()
                for usuario in usuarios:
                    destinatario = usuario.email
                    try:    #Para obtener la respuesta si la hay
                        variables = Comensal.objects.get(user=usuario)
                        tipo = variables.opciones

                        #Para las fechas
                        numdias = ["","","","","","",""]
                        today = date.today()
                        for i in range (7):
                            num1 = today + timedelta(days=i)
                            num1 = num.strftime('%d/%m/%Y')
                            numdias[i] = str(num1)
                        num_day = today.weekday()
                        dias = ["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"]
                        j = 0
                        for i in range(num_day,7,1):
                            dias[i] = dias[i] + " (" + numdias[j] + ")"
                            j = j + 1
                        for i in range(0,num_day,1):
                            dias[i] = dias[i] + " (" + numdias[j] + ")"
                            j = j + 1

                        subject = 'Correo semanal del Parte'
                        context =  {'variables': variables, 'tipo': tipo, 'dias': dias}
                        html_message = render_to_string('blog/mailparte.html', {'context': context})
                        plain_message = strip_tags(html_message)
                        from_email = EMAIL_HOST_USER
                        #from_email = 'noreply@partebcn.com'
                        to = destinatario
                        mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
                    except Comensal.DoesNotExist:
                        hola = 'N'

            elif request.POST.get("dianuevo"):
                newday = request.POST.get('selectday','')
                num = days.index(newday)
                diap.diaparte = num
        diap.save()
        currentday = days[num]
        return render(request, 'blog/imprimir.html', {'title': 'Imprimir', 'days': days, 'currentday': currentday})
    else:
        return render(request, 'blog/inicio.html', {'title': 'Inicio'})

@login_required
def Metaverso(request):
    return render(request, 'blog/metaverso.html', {'title': 'Metaverso'})

@login_required
def Recursos(request):
    recursos = Recurso.objects.all()
    directory = []
    variables = []
    for recurso in recursos:
        directory = "../media/" + str(recurso.recurso)
        variables.append([directory,recurso])
    return render(request, 'blog/recursos.html', {'title': 'Recursos', 'variables': variables})

@login_required
def NuevoRecurso(request):
    error = ""
    if request.method == 'POST':
        titulo = ""
        descripcion = ""
        try:
            if request.FILES['myfile']:
                archivo = request.FILES['myfile']
                try:
                    imagen = request.FILES['preview']
                except:
                    error = "Introduzca una imagen de vista previa (puedes hacer una captura de cualquier parte del archivo)"
                try:
                    titulo = request.POST.get('nombre', '')
                    if titulo == "":
                        error = "Introduzca un título"
                except:
                    error = "Introduzca un título"
                try:
                    descripcion = request.POST.get('descripcion', '')
                    if descripcion == "":
                        error = "Introduzca una descripción"
                except:
                    error = "Introduzca una descripción"
                #fs = FileSystemStorage()
                #filename = fs.save(myfile.name, myfile)
                #uploaded_file_url = fs.url(archivo)
                if error == "":
                    nuevo = Recurso(titulo=titulo,descripcion=descripcion,imagen=imagen,recurso=archivo)
                    nuevo.save() #guarda la nueva respuesta en la base de datos
                #return render(request, 'blog/recursos.html', {'title': 'Recursos', 'uploaded_file_url' : uploaded_file_url})
        except:
            error = "Archivo no subido"
        if error != "":
            return render(request, 'blog/recursonuevo.html', {'title': 'Nuevo Recurso', 'error': error, 'titulo': titulo, 'descripcion': descripcion})
        else:
            recursos = Recurso.objects.all()
            directory = []
            variables = []
            for recurso in recursos:
                directory = "../media/" + str(recurso.recurso)
                variables.append([directory,recurso])
            return render(request, 'blog/recursos.html', {'title': 'Recursos', 'variables': variables})
    else:
        return render(request, 'blog/recursonuevo.html', {'title': 'Nuevo Recurso', 'error': error})