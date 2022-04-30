import sqlite3
#from turtle import end_fill
from django.shortcuts import render, get_object_or_404
import sys
sys.path.append("..")# Adds higher directory to python modules path.
sys.path.append("./blog")
#settings.configure()
#from ..ParteWebpagedjango.settings import EMAIL_HOST_USER
from models import Deportista, Post, Comensal, Dia1, VariablesGlobales, Recurso
from django.core.mail import send_mail
from django.utils.html import strip_tags
from datetime import date   #Para saber la fecha
from datetime import datetime, timedelta   #Para saber la fecha

#Email with dynamic content
from django.core import mail
from django.template.loader import render_to_string

#Para almacenar archivos
from django.conf import settings
from django.core.files.storage import FileSystemStorage


today = date.today()
num_day = today.weekday()
try:
    diap = VariablesGlobales.objects.get()
except VariablesGlobales.DoesNotExist:
    diap = VariablesGlobales(diadxt=6,diaparte=6)
    diap.save()

diap.diaparte = num_day
diap.save()