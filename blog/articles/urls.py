from django.urls import path
from .views import archives, ArticleListView, ArticleDetailView, live_search

urlpatterns = [
    path('archives/', archives, name='archives'),
    path('', ArticleListView.as_view(), name='article_list'),
    path('<slug:slug>/', ArticleDetailView.as_view(), name='article_detail'),
    path('live-search/', live_search, name="live_search"),
]
