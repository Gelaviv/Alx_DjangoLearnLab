# posts/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Post, Comment
from .serializers import (
    PostSerializer, PostCreateSerializer, 
    CommentSerializer, CommentCreateSerializer
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['title', 'content']
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return PostCreateSerializer
        return PostSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def comment(self, request, pk=None):
        post = self.get_object()
        serializer = CommentCreateSerializer(data=request.data)
        
        if serializer.is_valid():
            comment = Comment.objects.create(
                post=post,
                author=request.user,
                content=serializer.validated_data['content']
            )
            return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
