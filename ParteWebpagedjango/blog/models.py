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

class Deportista(models.Model):
    msg_id = models.AutoField(primary_key=True,default=None)
    user = models.CharField(max_length=100, default="")
    observaciones = models.CharField(max_length=150, default="")
    dxt = models.CharField(max_length=1, default="N")

    def __str__(self):
        return self.user


#class Contact(models.Model):
#    msg_id = models.AutoField(primary_key=True)
#    user = models.CharField(max_length=100, default="")
#    observaciones = models.CharField(max_length=150, default="")
#    dxt = models.CharField(max_length=1, default="N")

#    def __str__(self):
#        return self.user
