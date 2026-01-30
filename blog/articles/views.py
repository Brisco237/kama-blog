from django.shortcuts import render, redirect
from .models import Category, Article, Comment, Subscription
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
import re
import json


# Create your views here.
def archives(request):
    articles = Article.objects.all()
    nb_article = articles.count()
    categories = Category.objects.all()

    return render(request, 'articles/archives.html', 
    {'categories': categories, 'nb_article' : nb_article, 
    'articles' : articles })

class ArticleListView(ListView):
    model = Article
    template_name = 'articles/article_list.html'
    context_object_name = 'articles'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()

        return context


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
        
        # Ajouter le statut d'abonnement
        if self.request.user.is_authenticated:
            try:
                context['is_subscribed'] = self.request.user.subscription.is_subscribed
            except Subscription.DoesNotExist:
                context['is_subscribed'] = False
        
        return context

    #nombres de vues de l'article
    """def get_object(self):
        article = super().get_object()
        article.vues += 1
        article.save()

        key = f"viewed_article_{article.id}"
        if not self.request.session.get(key):
            article.vues += 1
            article.save()
            self.request.session[key] = True 

        return article"""

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


def get_articles_by_category(request):
    categories = Category.objects.all()
    data = {}
    
    for category in categories:
        articles = Article.objects.filter(category=category, status='published').values(
            'id', 'title', 'slug', 'summary', 'created_at', 'vues', 'img'
        )
        data[category.slug] = {
            'name': category.name,
            'articles': list(articles)
        }
    
    return JsonResponse(data)
