from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ('id', 'username', 'email', 'role', 'phone_number', 'company', 'is_staff', 'is_active', 'last_login')
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'phone_number', 'company')
    ordering = ('username',)
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email', 'phone_number', 'company')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
        ('Role', {
            'fields': ('role',)
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'role', 'phone_number', 'company', 'password1', 'password2'),
        }),
    )
