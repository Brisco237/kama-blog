from django.contrib import admin
from .models import Article, Category, Comment, Source, Subscription


# Register your models here.
@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ("article", "number")
    ordering = ("article", "number")
    list_filter = ("article",)
    search_fields = ("reference", "article__title")

admin.site.register(Article)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Subscription)

admin.site.site_header = "Kama-Blog Administration"
admin.site.site_title = "Kama-Blog Admin"
admin.site.index_title = "Tableau de bord"