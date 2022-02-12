from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from ParteWebpagedjango.settings import SECURITY_CODE, EMAIL_HOST_USER
from django.core.mail import send_mail
from django.utils.html import strip_tags


def codigoseguridad(request):
    if request.method == 'POST':
        codigointroducido = request.POST.get('codigo', '')
        if codigointroducido == SECURITY_CODE:
            nombre = request.POST.get('nombre', '')
            html = """<html>
                        <body>
                                <h4>¡Buenos días!</h4>
                                <h4></h4>
                                """ + nombre + """</h3><h4> se ha registrado en la página web</h4><br>
                                <h4>¿Conoces a este usuario? Entra en el siguiente enlace para gestionar su perfil: https://partebarcelona.pythonanywhere.com/admin/auth/user/</h4>
                                <h4>No contestar a este correo, se ha generado automáticamente.</h4>
                                <h4>Atentamente,</h4>
                                <h4></h4>
                                <h4>Equipo del Parte</h4>
                        </body>
                        </html> """
            
            mensaje = strip_tags(html)
            send_mail('Nuevo usuario registrado',
            mensaje,
            EMAIL_HOST_USER,
            [EMAIL_HOST_USER],
            fail_silently=False)
            return redirect('register')
        else:
           return render(request, 'users/codigoseguridad.html') 
    else:
        return render(request, 'users/codigoseguridad.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required     #To avoid not login users to enter in a profile directly with the link
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)

#Kinds of message: 
#messages.debug
#messages.info
#messages.success
#messages.warning
#messages.error
