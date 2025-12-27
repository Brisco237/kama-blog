from django.shortcuts import render
from .models import Category

# Create your views here.
def archives(request):
    categories = Category.objects.all()
    return render(request, 'articles/archives.html', {'categories': categories})