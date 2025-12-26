from django.contrib import admin
from .models import User, Profile

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_active', 'is_staff')

admin.site.register(User, UserAdmin)
admin.site.register(Profile)