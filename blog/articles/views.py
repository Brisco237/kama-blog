from django.shortcuts import render
from .models import Category, Article

# Create your views here.
def archives(request):
    articles = Article.objects.all()
    nb_article = articles.count()
    categories = Category.objects.all()
    return render(request, 'articles/archives.html', {'categories': categories, 'nb_article' : nb_article, 'articles' : articles})