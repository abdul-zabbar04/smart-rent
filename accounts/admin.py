from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin

class CustomAdmin(UserAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email', 'is_staff', 'profile_image']
    # ADD 'fieldsets' to handle custom user model fields
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('profile_image',)}),
    )

admin.site.register(CustomUser, CustomAdmin)
