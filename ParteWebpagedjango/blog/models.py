from tabnanny import verbose
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image

#from django.contrib.postgres.fields import ArrayField

class VariablesGlobales(models.Model):
    diadxt = models.IntegerField()
    #i = models.IntegerField(default=1)

    def __str__(self):
        return "Dia dxt: " + self.diadxt

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

class Deportista(models.Model):
    msg_id = models.AutoField(primary_key=True,default=None)
    #user = models.CharField(max_length=100, default="")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #user = models.OneToOneField(User, on_delete=models.CASCADE)
    observaciones = models.CharField(max_length=150, default="")
    dxt = models.CharField(max_length=1, default="N")

    def __str__(self):
        texto = self.user.username + " : " + self.dxt
        return texto 

class Dia1(models.Model):
    msg_id2 = models.AutoField(primary_key=True, default=None)
    b = models.CharField(max_length=50, default="-")
    l = models.CharField(max_length=50, default="-")
    d = models.CharField(max_length=50, default="-")
    m = models.CharField(max_length=50, default="-")

    def __str__(self):
        texto = self.b + " | " + self.l + " | " + self.d + " | " + self.m
        return texto   #Se podria poner un string con las 4 respuestas 

#L,M,X,J,V,S,D => días ; b,l,d,m => breakfast,lunch,dinner,mediamañana
class Comensal(models.Model):
    msg_id1 = models.AutoField(primary_key=True, default=None)
    #user = models.CharField(max_length=100, default="")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    opciones = models.CharField(max_length=25, default="")
#    Lb = models.CharField(max_length=100, default="")
#    Ll = models.CharField(max_length=100, default="")
#    Ld = models.CharField(max_length=100, default="")
#    Lm = models.CharField(max_length=100, default="")
    L = models.ForeignKey(Dia1, on_delete=models.CASCADE, related_name='L')
    M = models.ForeignKey(Dia1, on_delete=models.CASCADE, related_name='M')
    X = models.ForeignKey(Dia1, on_delete=models.CASCADE, related_name='X')
    J = models.ForeignKey(Dia1, on_delete=models.CASCADE, related_name='J')
    V = models.ForeignKey(Dia1, on_delete=models.CASCADE, related_name='V')
    S = models.ForeignKey(Dia1, on_delete=models.CASCADE, related_name='S')
    D = models.ForeignKey(Dia1, on_delete=models.CASCADE, related_name='D')
    
#    D = models.ForeignKey(Dia, on_delete=models.CASCADE)
#    D = ArrayField(models.CharField(max_length=25, default="-"),size=4)

    def __str__(self):
        return self.user.username

class Recurso(models.Model):
    id = models.AutoField(primary_key = True)
    titulo = models.CharField('Nombre', max_length = 255, blank = False, null = False)
    #fecha_publicacion = models.DateField('Fecha de publicación', blank = False, null = False)
    descripcion = models.TextField('Descripcion', null = True, blank = True)
    imagen = models.ImageField('Imagen', upload_to = 'FotosRecursos/', max_length = 255, null = True, blank = True)
    recurso = models.FileField('Archivo', upload_to = "recursos/", blank = True, null = True)
    fecha_creacion = models.DateField('Fecha de creación', auto_now = True, auto_now_add = False)

    class Meta:
        verbose_name = 'Recurso'
        verbose_name_plural = 'Recursos'
        ordering = ['fecha_creacion']

    def __str__(self):
        return self.titulo

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.imagen.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.imagen.path)

#class Contact(models.Model):
#    msg_id = models.AutoField(primary_key=True)
#    user = models.CharField(max_length=100, default="")
#    observaciones = models.CharField(max_length=150, default="")
#    dxt = models.CharField(max_length=1, default="N")

#    def __str__(self):
#        return self.user
