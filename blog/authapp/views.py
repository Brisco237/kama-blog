from django.shortcuts import render
from articles.models import Article

# Create your views here.
def home(request):
    articles = Article.objects.filter(status='published').order_by('published_at')
    article3 = Article.objects.all().first()
    article2 = articles[1] 
    article1 = articles[0]
    article4 = articles[3]
    article5 = articles[4]
    return render(request, 'authapp/home.html',
    {'article1': article1, 'article2': article2, 'article3': article3, 'article4': article4, 'article5': article5}
    )
