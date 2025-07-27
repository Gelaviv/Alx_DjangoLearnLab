from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.detail import DetailView
from .models import Library, Book
from django.contrib.auth.decorators import permission_required, login_required, user_passes_test
from .models import UserProfile
from django import forms


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author']



# Create your views here.
def list_books(request):
    books = Book.objects.all().select_related('author')
    can_add = request.user.has_perm('relationship_app.can_add_book')
    can_change = request.user.has_perm('relationship_app.can_change_book')
    can_delete = request.user.has_perm('relationship_app.can_delete_book')
    return render(request, 'relationship_app/list_books.html', {
        'books': books,
        'can_add': can_add,
        'can_change': can_change,
        'can_delete': can_delete
    })

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




@permission_required('relationship_app.can_add_book')
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_books')
    else:
        form = BookForm()
    return render(request, 'relationship_app/book_form.html', {'form': form})

@permission_required('relationship_app.can_change_book')
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('list_books')
    else:
        form = BookForm(instance=book)
    return render(request, 'relationship_app/book_form.html', {'form': form})

@permission_required('relationship_app.can_delete_book')
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('list_books')
    return render(request, 'relationship_app/book_confirm_delete.html', {'book': book})
