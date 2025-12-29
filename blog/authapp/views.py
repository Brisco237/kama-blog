from django.shortcuts import render
from articles.models import Article, Category

# Create your views here.
def home(request):
    articles = Article.objects.filter(status='published').order_by('published_at')
    categories = Category.objects.all()
    articles1 = Article.objects.filter(status='published').order_by('published_at')[:3]
    articles2 = Article.objects.filter(status='published')[:2]
    return render(request, 'authapp/home.html',
    {'articles1':articles1, 'categories': categories,
    'articles2':articles2
    }
    )

def register(request):
    return render(request, 'authapp/register.html')

def login_user(request):
    return render(request, 'authapp/login.html')
