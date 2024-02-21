from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from app_accounts.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'full_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'groups', 'is_email_verify')
    fieldsets = (
        (None, {'fields': ('password', 'comment')}),
        ('Personal info', {'fields': ('full_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_email_verify', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('full_name', 'email', 'password1', 'password2'),
        }),
    )
    search_fields = ('full_name', 'email', 'comment')
    ordering = ('date_joined',)

