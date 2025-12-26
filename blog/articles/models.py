from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.conf import settings

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, default='Histoire')
    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Article(models.Model):
    STATUS_CHOICES = (('draft', 'Brouillon'),('published', 'Publié'),)
    img = models.ImageField(upload_to='image_articles/', null=True, blank=True)
    title = models.CharField(max_length=255)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='articles', default=1)
    slug = models.SlugField(max_length=255, unique=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='articles')
    content = models.TextField()
    summary = models.TextField(blank=True)
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-published_at']
        verbose_name = "Article"
        verbose_name_plural = "Articles"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

