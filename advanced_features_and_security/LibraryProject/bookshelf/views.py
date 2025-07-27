
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required, login_required
from .models import Book
from django.core.exceptions import SuspiciousOperation
from django.db.models import Q  # For more complex safe queries
from .forms import BookForm


# Create your views here.

"""
Security Measures Implemented:
1. CSRF Protection: All forms include {% csrf_token %} and AJAX requests include CSRF header
2. XSS Protection: 
   - Django templates auto-escape variables
   - Manual escaping in form cleaning
   - CSP headers prevent inline scripts
3. SQL Injection Protection:
   - Only use Django ORM, never raw SQL with user input
4. Clickjacking Protection:
   - X-FRAME-OPTIONS set to DENY
   - CSP frame-ancestors set to 'none'
5. Secure Cookies:
   - CSRF and session cookies only sent over HTTPS
"""



@login_required
def book_list(request):

    """
    Secure book listing with search functionality.
    Uses Django ORM to prevent SQL injection.
    """
    books = Book.objects.all()
    search_query = request.GET.get('q', '').strip()
    if search_query:
        # Safe search using Django's ORM
        books = books.filter(
            Q(title__icontains=search_query) |
            Q(author__icontains=search_query)
        ).distinct()

    return render(request, 'bookshelf/book_list.html.html', {
        'books': books,
        'search_query': search_query,  # Pass back to template for display
        'can_add': request.user.has_perm('bookshelf.can_add_book'),
        'can_edit': request.user.has_perm('bookshelf.can_edit_book'),
        'can_delete': request.user.has_perm('bookshelf.can_delete_book')
    })


@permission_required('bookshelf.can_add_book')
def add_book(request):
# Handles book creation with CSRF protection via form template.
    
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'bookshelf/form_example.html', {'form': form})

@permission_required('bookshelf.can_edit_book')
def edit_book(request, pk):
    
    # Secure book editing with instance-specific permissions.
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'bookshelf/book_form.html', {'form': form})

@permission_required('bookshelf.can_delete_book')
def delete_book(request, pk):

    #Secure deletion with POST method requirement.
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})

def raise_exception(request):
    raise Exception("This is a test exception.")