
## Project Setup
Prerequisites
Python 3.8+

pip

virtualenv


Installation
bash
# Clone the project
git clone <repository-url>
cd social_media_api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install django djangorestframework django-cors-headers Pillow

# Apply migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Run server
python manage.py runserver
🔐 User Authentication
User Model
The custom user model extends Django's AbstractUser with additional fields:

python
class CustomUser(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.FileField(upload_to='profile_pics/', blank=True, null=True)
    followers = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='following')
Registration
Endpoint: POST /api/auth/register/

## Request:

json
{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "password2": "testpass123",
    "first_name": "Test",
    "last_name": "User",
    "bio": "User biography"
}
## Response:

json
{
    "token": "a1b2c3d4e5f6g7h8i9j0",
    "user_id": 1,
    "username": "testuser",
    "message": "User created successfully"
}
Login
Endpoint: POST /api/auth/login/

## Request:

json
{
    "username": "testuser",
    "password": "testpass123"
}
## Response:

json
{
    "token": "a1b2c3d4e5f6g7h8i9j0",
    "user_id": 1,
    "username": "testuser",
    "message": "Login successful"
}

## API Endpoints
Authentication Required Headers
http
Authorization: Token your_token_here
Content-Type: application/json
Posts Endpoints
1. # List All Posts
GET /api/posts/posts/
Query Parameters: ?page=2&search=keyword

## Response:

json
{
    "count": 15,
    "next": "http://localhost:8000/api/posts/posts/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "author": {
                "id": 1,
                "username": "testuser",
                "first_name": "Test",
                "last_name": "User"
            },
            "title": "My First Post",
            "content": "This is the content...",
            "created_at": "2024-01-15T10:30:00Z",
            "updated_at": "2024-01-15T10:30:00Z",
            "comments": [],
            "comment_count": 0
        }
    ]
}
2. # Create Post
POST /api/posts/posts/

## Request:

json
{
    "title": "New Post Title",
    "content": "This is the post content..."
}
## Response: (201 Created)

json
{
    "id": 2,
    "author": {
        "id": 1,
        "username": "testuser",
        "first_name": "Test",
        "last_name": "User"
    },
    "title": "New Post Title",
    "content": "This is the post content...",
    "created_at": "2024-01-15T11:30:00Z",
    "updated_at": "2024-01-15T11:30:00Z",
    "comments": [],
    "comment_count": 0
}
3. Get Single Post
GET /api/posts/posts/{id}/

## Response:

json
{
    "id": 1,
    "author": {
        "id": 1,
        "username": "testuser",
        "first_name": "Test",
        "last_name": "User"
    },
    "title": "My First Post",
    "content": "This is the content...",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z",
    "comments": [
        {
            "id": 1,
            "author": {
                "id": 2,
                "username": "otheruser",
                "first_name": "Other",
                "last_name": "User"
            },
            "content": "Great post!",
            "created_at": "2024-01-15T11:00:00Z",
            "updated_at": "2024-01-15T11:00:00Z"
        }
    ],
    "comment_count": 1
}
4. ## Update Post
PUT/PATCH /api/posts/posts/{id}/ (Author only)

## Request:

json
{
    "title": "Updated Title",
    "content": "Updated content..."
}
5. ## Delete Post
DELETE /api/posts/posts/{id}/ (Author only)

6. ## Add Comment to Post
POST /api/posts/posts/{id}/comment/

## Request:

json
{
    "content": "This is a comment on the post"
}
Response:

json
{
    "id": 2,
    "post": 1,
    "author": {
        "id": 1,
        "username": "testuser",
        "first_name": "Test",
        "last_name": "User"
    },
    "content": "This is a comment on the post",
    "created_at": "2024-01-15T12:00:00Z",
    "updated_at": "2024-01-15T12:00:00Z"
}

# Comments Endpoints
1. ## List All Comments
GET /api/posts/comments/

2. ## Create Comment
POST /api/posts/comments/

## Request:

json
{
    "post": 1,
    "content": "This is a direct comment"
}
3. ## Get Single Comment
GET /api/posts/comments/{id}/

4. ## Update Comment
PUT/PATCH /api/posts/comments/{id}/ (Author only)

5. ## Delete Comment
DELETE /api/posts/comments/{id}/ (Author only)

## Testing
Postman Collection
Import the following Postman collection:

json
{
  "info": {
    "name": "Social Media API",
    "description": "Complete API testing collection",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Authentication",
      "item": [
        {
          "name": "Register User",
          "request": {
            "method": "POST",
            "header": [
              {
                "key": "Content-Type",
                "value": "application/json"
              }
            ],
            "body": {
              "mode": "raw",
              "raw": "{\n    \"username\": \"testuser\",\n    \"email\": \"test@example.com\",\n    \"password\": \"testpass123\",\n    \"password2\": \"testpass123\",\n    \"first_name\": \"Test\",\n    \"last_name\": \"User\"\n}"
            },
            "url": {
              "raw": "{{base_url}}/api/auth/register/",
              "host": ["{{base_url}}"],
              "path": ["api", "auth", "register", ""]
            }
          }
        }
      ]
    }
  ]
}
Automated Testing
Run Django tests:

bash
python manage.py test accounts
python manage.py test posts
Manual Testing Script
python
# test_api.py
import requests
import json

BASE_URL = "http://localhost:8000"

def test_authentication():
    # Register user
    response = requests.post(f"{BASE_URL}/api/auth/register/", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123",
        "password2": "testpass123"
    })
    print("Registration:", response.status_code)
    
    # Login
    response = requests.post(f"{BASE_URL}/api/auth/login/", json={
        "username": "testuser",
        "password": "testpass123"
    })
    print("Login:", response.status_code)
    return response.json().get('token')

# Run tests
if __name__ == "__main__":
    token = test_authentication()
    print("Token:", token)
📁 Code Structure
text
social_media_api/
├── accounts/
│   ├── models.py          # CustomUser model
│   ├── serializers.py     # User serializers
│   ├── views.py          # Authentication views
│   └── urls.py           # Auth endpoints
├── posts/
│   ├── models.py         # Post and Comment models
│   ├── serializers.py    # Post and Comment serializers
│   ├── views.py          # CRUD operations
│   └── urls.py           # Post endpoints
└── social_media_api/
    ├── settings.py       # Django configuration
    └── urls.py          # Main URL routing



    Error Responses
Common Error Codes
400 Bad Request - Invalid input data

401 Unauthorized - Missing or invalid token

403 Forbidden - Permission denied

404 Not Found - Resource doesn't exist

Example Error Response
json
{
    "error": "Detailed error message here",
    "field_errors": {
        "field_name": ["Error description"]
    }
}