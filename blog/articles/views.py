from django.shortcuts import render, redirect
from .models import Category, Article, Comment
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.db.models import Q
import re


# Create your views here.
def archives(request):
    articles = Article.objects.all()
    nb_article = articles.count()
    categories = Category.objects.all()
    return render(request, 'articles/archives.html', 
    {'categories': categories, 'nb_article' : nb_article, 
    'articles' : articles
    }
    )

def search_articles(request):
    query = request.GET.get('query', '').strip()
    articles_search = []
    
    if query:
        articles_search = Article.objects.filter(
            (Q(title__icontains=query) | Q(category__name__icontains=query)),
            status='published'
        ).distinct()
    
    return render(request, 'articles/search_fragment.html', {'articles_search': articles_search, 'query': query })


class ArticleListView(ListView):
    model = Article
    template_name = 'articles/article_list.html'
    context_object_name = 'articles'
    paginate_by = 6


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'articles/article_detail.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = self.object
        context['related_articles'] = (Article.objects.filter(category=article.category).exclude(id=article.id))
        context['sources'] = article.sources.all().order_by('number')

        content = context["article"].content
        content = re.sub(
            r"\[\[(\d+)\]\]",
            r'<sup class="citation" data-ref="\1">\1</sup>',
            content
        )

        context["content"] = content
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        if not request.user.is_authenticated:
            messages.error(request, 'Vous devez être connecté pour ajouter un commentaire.')
            return redirect('article_detail', slug=self.object.slug)
    
        commentaire = request.POST.get('commentaire', '').strip()
        
        if not commentaire:
            messages.error(request, 'Le commentaire ne peut pas être vide.')
            return redirect('article_detail', slug=self.object.slug)
    
        Comment.objects.create(article=self.object,user=request.user,content=commentaire)
        messages.success(request, 'Votre commentaire a été ajouté avec succès!')
        return redirect('article_detail', slug=self.object.slug)

