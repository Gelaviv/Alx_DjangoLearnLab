from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.detail import DetailView
from .models import Library, Book
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import UserProfile

# Create your views here.
def list_books(request):
    books = Book.objects.all().select_related('author')  # Optimize query
    return render(request, 'relationship_app/list_books.html', {'books': books})


class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

    def get_queryset(self):
        return Library.objects.prefetch_related('books__author')
    

    def register(request):
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('list_books')
        else:
            form = UserCreationForm()
        return render(request, 'relationship_app/register.html', {'form': form})
    

def check_role(user, required_role):
    try:
        return user.userprofile.role == required_role
    except UserProfile.DoesNotExist:
        return False

# Admin View
@login_required
@user_passes_test(lambda u: check_role(u, 'ADMIN'))
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

# Librarian View
@login_required
@user_passes_test(lambda u: check_role(u, 'LIBRARIAN'))
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

# Member View
@login_required
@user_passes_test(lambda u: check_role(u, 'MEMBER'))
def member_view(request):
    return render(request, 'relationship_app/member_view.html')