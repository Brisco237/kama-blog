from django.shortcuts import render, redirect
from articles.models import Article, Category
from django.conf import settings
from django.contrib import messages
from .models import Profile, User

# Create your views here.
def home(request):
    categories = Category.objects.all()
    articles1 = Article.objects.filter(status='published').order_by('published_at')[:3]
    articles2 = Article.objects.filter(status='published')[:3]
    return render(request, 'authapp/home.html',
    {'articles1':articles1, 'categories': categories,
    'articles2':articles2
    }
    )

def register(request):
    if request.method == "POST":
        photo = request.FILES['photo']
        username = request.POST['name']
        last_name = request.POST['subname']
        email = request.POST['email']
        password  = request.POST['password']
    
    try:
        user = User.objects.create_user(
            username=username, last_name=last_name, email=email, password=password
        )
    
        Profile.objects.create(user=user, photo=photo)
        messages.success(request, "Compte créé avec succès!")
        return redirect('login_user')
        
    except Exception as e:
        messages.error(request, f"Erreur: {str(e)}")
    

    return render(request, 'authapp/register.html')

def login_user(request):
    return render(request, 'authapp/login.html')

