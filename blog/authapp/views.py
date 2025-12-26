from django.shortcuts import render
from articles.models import Article, Category

# Create your views here.
def home(request):
    articles = Article.objects.filter(status='published').order_by('published_at')
    categories = Category.objects.all()
    article1 = articles[0]
    article2 = articles[1] 
    article3 = articles[2]
    article4 = articles[3]
    article5 = articles[4]
    return render(request, 'authapp/home.html',
    {'article1': article1, 'article2': article2, 'article3': article3, 
    'article4': article4, 'article5': article5, 'categories': categories
    }
    )

def register(request):
    return render(request, 'authapp/register.html')

def login_user(request):
    return render(request, 'authapp/login.html')
