from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm

from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
        "username",
        "email",        
        "first_name",
        "last_name",
        "is_staff",
    ]
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ('profile_pic',)}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {
        "fields": ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'profile_pic',)
    }),)