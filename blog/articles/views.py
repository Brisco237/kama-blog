from django.shortcuts import render
from .models import Category, Article
from django.views.generic import ListView, DetailView

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

        context['related_articles'] = (
            Article.objects
            .filter(category=article.category)
            .exclude(id=article.id)
        )

        return context
