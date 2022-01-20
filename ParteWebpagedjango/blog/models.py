from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

class Depor(models.Model):
    hace = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.hace

    def get_absolute_url(self):
        return reverse('depor-detail', kwargs={'pk': self.pk})

class Deportista(models.Model):
    name = models.CharField(max_length=50, default='')
    #respuesta=models.CharField(max_length=100, default='')

    def __str__(self):
        return self.name
        #return self.respuesta


class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    user = models.CharField(max_length=100, default="")
#    email = models.CharField(max_length=70, default="")
#    phone = models.CharField(max_length=70, default="")
#    desc = models.CharField(max_length=500, default="")


    def __str__(self):
        return self.name
