from django.urls import path
from .views import archives, ArticleListView, ArticleDetailView, search_articles

urlpatterns = [
    path('archives/', archives, name='archives'),
    path('search/', search_articles, name='search'),
    path('', ArticleListView.as_view(), name='article_list'),
    path('<slug:slug>/', ArticleDetailView.as_view(), name='article_detail'),
]
