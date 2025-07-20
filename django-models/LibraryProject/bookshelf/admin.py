from django.contrib import admin
from .models import Book



class BookAdminConfig(admin.ModelAdmin):
    list_filter = ('title', 'author', 'publication_year')
    search_fields = ('title', 'author', 'publication_year')



# Register your models here.
admin.site.register(Book, BookAdminConfig)



    