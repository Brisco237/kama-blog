from django.shortcuts import render, redirect
from articles.models import Article, Category
from django.conf import settings
from django.contrib import messages
from .models import Profile, User
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from allauth.socialaccount.models import SocialAccount, SocialApp

# Create your views here.
def google_login_callback(request):
    """
    Callback pour les connexions Google
    Intercepte le flux de google et redirige vers le formulaire d'inscription personnalisé
    """
    # Vérifier si c'est une tentative de connexion Google
    if request.session.get('google_login'):
        return redirect('register')
    return redirect('login_user')
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
    # Si l'utilisateur vient de Google
    google_email = request.session.get('google_email')
    google_first_name = request.session.get('google_first_name')
    
    if request.method == "POST":
        photo = request.FILES.get('photo')
        username = request.POST['name']
        last_name = request.POST['subname']
        email = request.POST['email']
        password  = request.POST['password']
        
        # Validation des champs
        if User.objects.filter(username=username).exists():
            messages.error(request,"Ce username est deja utilisé !")
            return redirect('register')
        
        if not username.isalpha():
            messages.error(request, "Désolé, mais le username doit etre en lettre uniquement alphanumérique!")
            return redirect('register') 
        
        if User.objects.filter(email=email).exists():
            messages.error(request,"Cet adresse email est deja utilisé !")
            return redirect('register')
        
        # Validation du mot de passe
        try: 
            validate_password(password)
        except ValidationError as errors:
            for error in errors:
                messages.error(request, str(error))
            context = {
                'google_email': google_email,
                'google_first_name': google_first_name,
                'email': email,
                'username': username,
                'last_name': last_name
            }
            return render(request, 'authapp/register.html', context)
        
        # Vérifier si photo est fournie
        if not photo and not google_email:  # Photo requise sauf si vient de Google
            messages.error(request, "Vous devez ajouter une photo de profil!")
            return redirect('register')
        
        try:
            user = User.objects.create_user(
                username=username, 
                last_name=last_name, 
                email=email, 
                password=password
            )
            
            # Créer le profil
            if photo:
                Profile.objects.create(user=user, photo=photo)
            else:
                Profile.objects.create(user=user)  # Sans photo si vient de Google
            
            # Nettoyer la session Google
            if 'google_email' in request.session:
                del request.session['google_email']
            if 'google_first_name' in request.session:
                del request.session['google_first_name']
            
            # Connecter l'utilisateur et rediriger
            login(request, user)
            messages.success(request, "Compte créé avec succès!")
            return redirect('home')
        
        except Exception as e:
            messages.error(request, f"Erreur: {str(e)}")
            return redirect('register')

    # Préparer le contexte pour le formulaire
    context = {
        'google_email': google_email,
        'google_first_name': google_first_name,
    }
    return render(request, 'authapp/register.html', context)

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
            return redirect('login_user')

    return render(request, 'authapp/login.html')

def logout_user(request):
    messages.success(request, "Vous avez été déconnecté !")
    logout(request)
    return redirect('home')

