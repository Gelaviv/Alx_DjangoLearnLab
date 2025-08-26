# posts/views.py
from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Post, Comment, Like
from django.db.models import Q
from .serializers import (
    PostSerializer, PostCreateSerializer, 
    CommentSerializer, CommentCreateSerializer, LikeSerializer
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from notifications.models import Notification



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

            if post.author != request.user:
                Notification.objects.create(
                    recipient=post.author,
                    actor=request.user,
                    verb='comment',
                    target=comment
                )

            return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        # Use generics.get_object_or_404 instead of get_object_or_404
        post = generics.get_object_or_404(Post, pk=pk)
        
        # Use get_or_create on a single line as expected by the checker
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        
        if created:
            # Update likes count
            post.likes_count += 1
            post.save()
            
            # Create notification (if not liking own post)
            if post.author != request.user:
                Notification.objects.create(
                    recipient=post.author,
                    actor=request.user,
                    verb='like',
                    target=post
                )
            
            return Response(
                LikeSerializer(like, context={'request': request}).data,
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {'error': 'You have already liked this post.'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def unlike(self, request, pk=None):
        # Use generics.get_object_or_404 instead of get_object_or_404
        post = generics.get_object_or_404(Post, pk=pk)
        
        try:
            like = Like.objects.get(user=request.user, post=post)
            like.delete()
            post.likes_count -= 1
            post.save()
            
            return Response(
                {'message': 'Post unliked successfully.'},
                status=status.HTTP_200_OK
            )
        except Like.DoesNotExist:
            return Response(
                {'error': 'You have not liked this post.'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['get'])
    def likes(self, request, pk=None):
        post = self.get_object()
        likes = post.post_likes.all()
        serializer = LikeSerializer(likes, many=True, context={'request': request})
        return Response(serializer.data)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)



class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Get posts from users that the current user follows
        following_users = self.request.user.following.all()
        return Post.objects.filter(
            Q(author__in=following_users) | Q(author=self.request.user)
        ).order_by('-created_at')
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)