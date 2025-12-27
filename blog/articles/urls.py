from django.urls import path
from .views import archives, ArticleListView, ArticleDetailView

urlpatterns = [
    path('archives/', archives, name='archives'),
    path('', ArticleListView.as_view(), name='article_list'),
    path('<slug:slug>/', ArticleDetailView.as_view(), name='article_detail'),
]
