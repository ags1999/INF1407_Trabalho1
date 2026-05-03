from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Livro

class CustomUserAdmin(UserAdmin):
    # Define which fields to display in the list view
    list_display = ('email', 'username', 'is_staff', 'is_active')
    # Define which fields are used to order the list
    ordering = ('email',)

admin.site.register(User, CustomUserAdmin)
admin.site.register(Livro)