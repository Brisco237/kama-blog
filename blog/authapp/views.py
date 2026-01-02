from django.shortcuts import render, redirect
from articles.models import Article, Category
from django.conf import settings
from django.contrib import messages
from .models import Profile, User
from django.contrib.auth import authenticate, login, logout

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
    
        if User.objects.filter(username=username):
            messages.error(request,"Ce username est deja utilisé !")
            return redirect('register')
        if not username.isalpha():
            messages.error(request, "Désolé, mais le username doit etre en lettre uniquement alphanumérique!")
            return redirect('register') 
        if User.objects.filter(email=email):
            messages.error(request,"Cet adresse email est deja utilisé !")
            return redirect('register') 
            
        try: 
            validate_password(password)
        except ValidationError as errors:
            messages.error(request, f'{errors}')
            return render(request, 'authapp/register.html',{'errors':errors})

    return render(request, 'authapp/register.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST['name']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Bienvenue {user.username} Vous etes connectez !")
            return redirect('home')
        else:
            messages.error(request, "Mot de passe ou nom d'utilisateur incorrect !")
            return redirect('login.html')

    return render(request, 'authapp/login.html')

def logout_user(request):
    logout(request)
    return redirect('home')

