import sqlite3
import sys
sys.path.append("..")# Adds higher directory to python modules path.
from django.contrib.auth.models import User
from ParteWebpagedjango.settings import EMAIL_HOST_USER
from .models import Deportista
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.contrib.auth.models import User

def main():
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
    data = "Mail enviado correctamente"
    return data