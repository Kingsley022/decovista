from django.contrib import admin
from .models import User, UserDetails, DesignerDetails

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'email', 'role', 'is_active']
    list_filter = ['role', 'username']


@admin.register(UserDetails)
class UserDetailsAdmin(admin.ModelAdmin):
    list_display = ['user_id__username', 'contact_number', 'address']


@admin.register(DesignerDetails)
class DesignerDetailsAdmin(admin.ModelAdmin):
    list_display = ['user_details__username', 'years_of_experience', 'specializations']
    