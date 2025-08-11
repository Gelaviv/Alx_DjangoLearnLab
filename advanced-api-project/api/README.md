# Advanced API Project Documentation

## API Endpoints

### Books
- `GET /api/books/` - List all books (filterable, searchable, sortable)
- `POST /api/books/` - Create new book (authenticated only)
- `GET /api/books/{id}/` - Get book details
- `PUT/PATCH /api/books/{id}/` - Update book (authenticated only)
- `DELETE /api/books/{id}/` - Delete book (authenticated only)

### Authors
- `GET /api/authors/` - List all authors
- `POST /api/authors/` - Create new author (authenticated only)
- `GET /api/authors/{id}/` - Get author details
- `PUT/PATCH /api/authors/{id}/` - Update author (authenticated only)
- `DELETE /api/authors/{id}/` - Delete author (authenticated only)

## Authentication
- Read operations: No authentication required
- Write operations: Require token authentication

## Filtering and Searching
Books endpoint supports:
- Filter by publication_year or author: `?publication_year=2023`
- Search by title or author name: `?search=harry`
- Ordering: `?ordering=-publication_year` (descending)
- Minimum year filter: `?min_year=2000`

## Custom Permissions
- Admins can perform all operations
- Regular users can only modify their own content (if ownership is implemented)
- Unauthenticated users can only read