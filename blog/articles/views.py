from django.shortcuts import render, redirect
from .models import Category, Article, Comment, Subscriber
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
import re
import json
from django.core.mail import send_mail
from django.http import HttpResponse
from django.core.mail import EmailMultiAlternatives
from authapp.models import User


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
        return context

    #nombres de vues de l'article
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        cookie_name = f"viewed_article_{self.object.pk}"

        response = super().get(request, *args, **kwargs)

        if not request.COOKIES.get(cookie_name):
            self.object.vues += 1
            self.object.save(update_fields=["vues"])
            response.set_cookie(cookie_name, "true", max_age=86400)

        return response

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


def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email-subscribers')
        if email:
            if Subscriber.objects.filter(email=email).exists():
                messages.error(request, 'Cet email est déjà inscrit à la newsletter.')
            else:
                Subscriber.objects.create(email=email)
                messages.success(request, 'Merci ! Vous êtes maintenant abonné.')
        else:
            messages.error(request, 'Veuillez entrer une adresse email valide.')

        return redirect(request.META.get('HTTP_REFERER', 'home'))
    return redirect('home')
