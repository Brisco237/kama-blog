from django.contrib import admin
from .models import Article, Category, Comment

# Register your models here.
admin.site.register(Article)
admin.site.register(Category)
admin.site.register(Comment)

admin.site.site_header = "Kama-Blog Administration"
admin.site.site_title = "Kama-Blog Admin"
admin.site.index_title = "Tableau de bord"