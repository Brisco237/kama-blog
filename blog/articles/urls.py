from django.urls import path
from .views import archives, ArticleListView, ArticleDetailView, get_articles_by_category, newsletter_subscribe

urlpatterns = [
    path('archives/', archives, name='archives'),
    path('api/articles-by-category/', get_articles_by_category, name='get_articles_by_category'),
    path('subscribe-newsletter/', newsletter_subscribe, name='newsletter_subscribe'),
    path('', ArticleListView.as_view(), name='article_list'),
    path('<slug:slug>/', ArticleDetailView.as_view(), name='article_detail'),
]
