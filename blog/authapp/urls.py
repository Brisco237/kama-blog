from django.urls import path
from .views import home, register, login_user, logout_user, contact, recent, populaire

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_user, name='login_user'),
    path('logout/', logout_user, name='logout_user'),
    path('contact/', contact, name='contact'),
]
