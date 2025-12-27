from django.shortcuts import render

# Create your views here.
def archives(request):
    return render(request, 'articles/archives.html')