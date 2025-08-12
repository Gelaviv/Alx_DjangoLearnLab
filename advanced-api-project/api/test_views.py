from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from api.models import Book, Author 
from rest_framework.authtoken.models import Token



class BookAPITestCase(APITestCase):
    def setUp(self):
        # Create test users
        self.admin_user = User.objects.create_superuser(
            username='admin',
            password='adminpass',
            email='admin@example.com'
        )
        self.regular_user = User.objects.create_user(
            username='user',
            password='userpass',
            email='user@example.com'
        )
        
        # Create tokens
        self.admin_token = Token.objects.create(user=self.admin_user)
        self.user_token = Token.objects.create(user=self.regular_user)
        
        # Create test author
        self.author = Author.objects.create(name='J.K. Rowling')
        
        # Create test books
        self.book1 = Book.objects.create(
            title='Harry Potter 1',
            publication_year=1997,
            author=self.author
        )
        self.book2 = Book.objects.create(
            title='Harry Potter 2',
            publication_year=1998,
            author=self.author
        )
        
        # Initialize client
        self.client = APIClient()

    def test_login_authentication(self):
        """Test that demonstrates using self.client.login()"""
        # Test login with regular user
        login_success = self.client.login(username='user', password='userpass')
        self.assertTrue(login_success)
        
        # Test making an authenticated request
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Logout
        self.client.logout()



    # Book Creation Tests

    def test_create_book_authenticated(self):
            url = reverse('book-list')
            data = {
            'title': 'New Book',
            'publication_year': 2023,
            'author': self.author.id
        }
            self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token.key}')
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(Book.objects.count(), 3)
            self.assertEqual(Book.objects.last().title, 'New Book')

    def test_create_book_unauthenticated(self):
        url = reverse('book-list')
        data = {
            'title': 'New Book',
            'publication_year': 2023,
            'author': self.author.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

# Book Retrieval Tests

    def test_get_book_list(self):
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # We created 2 books in setUp

    def test_get_single_book(self):
        url = reverse('book-detail', kwargs={'pk': self.book1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Harry Potter 1')

    
    # Book Update Tests
    '''def test_update_book_owner(self):
        url = reverse('book-detail', kwargs={'pk': self.book1.id})
        data = {'title': 'Updated Title'}
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token.key}')
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Title')'''

    def test_update_book_unauthenticated(self):
        url = reverse('book-detail', kwargs={'pk': self.book1.id})
        data = {'title': 'Updated Title'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    
    # Book Deletion Tests
    def test_delete_book_admin(self):
        url = reverse('book-detail', kwargs={'pk': self.book1.id})
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.admin_token.key}')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    def test_delete_book_regular_user(self):
        url = reverse('book-detail', kwargs={'pk': self.book1.id})
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_token.key}')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    

    # Filtering Tests

    def test_filter_by_title(self):
        url = reverse('book-list') + '?title=Harry Potter 1'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Harry Potter 1')

    def test_filter_by_publication_year(self):
        url = reverse('book-list') + '?publication_year=1998'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Harry Potter 2')

    def test_filter_by_author_name(self):
        url = reverse('book-list') + '?author__name=J.K. Rowling'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)



# Searching Tests

    def test_search_by_title(self):
        url = reverse('book-list') + '?search=Potter 1'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Harry Potter 1')

    def test_search_by_author_name(self):
        url = reverse('book-list') + '?search=Rowling'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)



# Ordering Tests
    def test_order_by_title_ascending(self):
        url = reverse('book-list') + '?ordering=title'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, sorted(titles))

    def test_order_by_publication_year_descending(self):
        url = reverse('book-list') + '?ordering=-publication_year'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, sorted(years, reverse=True))