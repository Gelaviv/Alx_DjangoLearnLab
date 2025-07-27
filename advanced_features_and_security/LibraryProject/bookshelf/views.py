
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required, login_required
from .models import Book
from django import forms


# Create your views here.

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author']

@login_required
def list_books(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/list_books.html', {
        'books': books,
        'can_add': request.user.has_perm('bookshelf.can_add_book'),
        'can_change': request.user.has_perm('bookshelf.can_change_book'),
        'can_delete': request.user.has_perm('bookshelf.can_delete_book')
    })

@permission_required('bookshelf.can_add_book')
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_books')
    else:
        form = BookForm()
    return render(request, 'bookshelf/book_form.html', {'form': form})

@permission_required('bookshelf.can_change_book')
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('list_books')
    else:
        form = BookForm(instance=book)
    return render(request, 'bookshelf/book_form.html', {'form': form})

@permission_required('bookshelf.can_delete_book')
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('list_books')
    return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})