from rest_framework import serializers
from .models import Author, Book
from datetime import datetime



class BookSerializer(serializers.ModelSerializer):
    
    """
    Serializer for the Book model that includes all fields.
    Includes custom validation to ensure publication year is not in the future.
    """
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']

    def validate_publication_year(self, value):
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value



class AuthorSerializer(serializers.ModelSerializer):
    
    """
    Serializer for the Author model that includes the name field
    and a nested representation of related books using BookSerializer.
    The books field is read-only and dynamically includes all books by the author.
    """
    
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        
        model = Author
        fields = ['id', 'name', 'books']