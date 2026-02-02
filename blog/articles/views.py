from django.shortcuts import render, redirect
from .models import Category, Article, Comment, NewsletterSubscriber
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


def newsletter_subscribe(request):
    if request.method == "POST":
        email = request.POST.get("email-subscribers")
        subscriber, created = NewsletterSubscriber.objects.get_or_create(email=email)
        
        if created:
            subject = "Bienvenue sur Kama-Blog 📰"
            from_email = "Kama Blog <kamdembrice770@gmail.com>"
            text_content = "Merci pour votre abonnement à Kama-Blog !"
            
            html_content = f"""
            <!DOCTYPE html>
            <html>
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                </head>
                <body style="margin: 0; padding: 0; font-family:Arial, sans-serif;">
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px 20px;">
                        <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 15px; overflow: hidden; box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);">
                            
                            <!-- Header -->
                            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px 20px; text-align: center;">
                                <h1 style="color: #ffffff; margin: 0; font-size: 32px; font-weight: bold;">🎉 Bienvenue sur Kama-Blog !</h1>
                                <p style="color: #f0f0f0; margin: 10px 0 0 0; font-size: 16px;">Merci de nous avoir rejoints</p>
                            </div>
                            
                            <!-- Main Content -->
                            <div style="padding: 40px 30px; color: #333333;">
                                <p style="font-size: 16px; line-height: 1.6; margin: 0 0 20px 0;">
                                    Salut,
                                </p>
                                
                                <p style="font-size: 16px; line-height: 1.6; margin: 0 0 20px 0;">
                                    Nous sommes ravi de vous compter parmi nos abonnés ! 🌟
                                </p>
                                
                                <div style="background-color: #f8f9fa; border-left: 4px solid #667eea; padding: 20px; margin: 30px 0; border-radius: 5px;">
                                    <p style="font-size: 15px; line-height: 1.6; margin: 0; color: #555555;">
                                        Vous recevrez désormais <strong>nos articles les plus intéressants</strong> directement dans votre boîte mail. 
                                        Restez informé des dernières actualités, tutoriels et analyses du blog.
                                    </p>
                                </div>
                                
                                <p style="font-size: 16px; line-height: 1.6; margin: 0 0 30px 0;">
                                    À bientôt sur <strong>Kama-Blog</strong> ! 📝
                                </p>
                            </div>
                            <!-- Footer -->
                            <div style="background-color: #f8f9fa; padding: 30px; text-align: center; border-top: 1px solid #e0e0e0;">
                                <p style="font-size: 14px; color: #999999; margin: 0 0 15px 0;">
                                    © 2026 Kama-Blog. Tous droits réservés.
                                </p>
                                <p style="font-size: 12px; color: #aaaaaa; margin: 0;">
                                    Vous recevez cet email parce que vous vous êtes abonné à notre newsletter.
                                </p>
                            </div>
                        </div>
                    </div>
                </body>
            </html>
            """
            
            msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            
            messages.success(request, "Inscription réussie 🎉 ! Vérifiez votre email 📩")
            return redirect(request.META.get("HTTP_REFERER", "/"))
        else:
            messages.error(request, "Désolé mais cet email est déjà inscrit à la newsletter ! Entrez en une autre. 😊")

    return redirect(request.META.get("HTTP_REFERER", "/"))

