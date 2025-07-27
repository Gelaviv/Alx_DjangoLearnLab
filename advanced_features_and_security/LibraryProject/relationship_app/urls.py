from django.urls import path
from django.contrib.auth import views as auth_views
from .views import  register, add_book, edit_book, delete_book, list_books, LibraryDetailView
from .import views 



urlpatterns = [
   # Book and Library URLs
    path('books/', list_books, name='list_books'),
    path('add_book/', add_book, name='add_book'),
    path('edit_book/<int:pk>/', edit_book, name='edit_book'),
    path('delete_book/<int:pk>/', delete_book, name='delete_book'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),

    #  Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('register/', register, name='register'),


  # Role-based URLs
    path('admin/dashboard/', views.admin_view, name='admin_view'),
    path('librarian/dashboard/', views.librarian_view, name='librarian_view'),
    path('member/dashboard/', views.member_view, name='member_view')
]

