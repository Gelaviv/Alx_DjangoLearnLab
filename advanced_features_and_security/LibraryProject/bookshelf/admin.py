from django.contrib import admin
from .models import Book, CustomUser
from django.contrib.auth.admin import UserAdmin



class BookAdminConfig(admin.ModelAdmin):
    list_filter = ('title', 'author', 'publication_year')
    search_fields = ('title', 'author', 'publication_year')


class CustomUserAdmin(UserAdmin):
    # Fields to display in the user list
    list_display = ('username', 'email', 'date_of_birth', 'is_staff')
    # Fieldsets for the edit user page
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('email', 'date_of_birth', 'profile_photo')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}))
    
    # Fieldsets for the add user page
    add_fieldsets = ((None,{'classes': ('wide',), 'fields': ('username', 'email', 'date_of_birth', 'profile_photo', 'password1', 'password2')}))



# Register your models here.
admin.site.register(Book, BookAdminConfig)
admin.site.register(CustomUser, CustomUserAdmin)




    