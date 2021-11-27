from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

#Posts of the blog (Dictionaries)
posts = [
    {
        'author': 'CoreyMS',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'August 27, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'August 28, 2018'
    }
]


def home(request):
    context = {
        'posts': posts
    }
    return render(request, 'blog/home.html', context)    #To return a template rendered

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})   #title => tab title 



#def prueba2(request):
#   return HttpResponse('<h1>PAGINA PARA PROBAR</h1>')
    
