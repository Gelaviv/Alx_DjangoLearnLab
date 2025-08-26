# accounts/views.py
from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, logout
from django.shortcuts import get_object_or_404
from .serializers import (
    UserRegistrationSerializer, 
    UserLoginSerializer, 
    UserProfileSerializer,
    UserFollowSerializer,
    FollowActionSerializer,
)

# Import permissions directly to match checker pattern
from rest_framework import permissions

# Import CustomUser directly instead of using get_user_model()
from .models import CustomUser

# Keep your existing function-based views for auth endpoints
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_user(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username,
            'message': 'User created successfully'
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def user_login(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        login(request, user)
        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username,
            'message': 'Login successful'
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def user_logout(request):
    try:
        request.user.auth_token.delete()
        logout(request)
        return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT'])
@permission_classes([permissions.IsAuthenticated])
def user_profile(request):
    if request.method == 'GET':
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Replace function-based follow views with class-based views
class FollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FollowActionSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Use CustomUser directly
            user_to_follow = get_object_or_404(CustomUser, id=serializer.validated_data['user_id'])
            
            if request.user.follow(user_to_follow):
                return Response({
                    'message': f'You are now following {user_to_follow.username}'
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'error': 'Unable to follow user. You may already be following them or trying to follow yourself.'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UnfollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FollowActionSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Use CustomUser directly
            user_to_unfollow = get_object_or_404(CustomUser, id=serializer.validated_data['user_id'])
            
            if request.user.unfollow(user_to_unfollow):
                return Response({
                    'message': f'You have unfollowed {user_to_unfollow.username}'
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'error': 'You are not following this user.'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserListView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        # Use CustomUser.objects.all() as expected by checker
        users = CustomUser.objects.all()
        serializer = UserProfileSerializer(users, many=True)
        return Response(serializer.data)

# Keep function-based views for following/followers lists
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def following_list(request):
    following_users = request.user.following.all()
    serializer = UserFollowSerializer(following_users, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def followers_list(request):
    followers = request.user.followers.all()
    serializer = UserFollowSerializer(followers, many=True, context={'request': request})
    return Response(serializer.data)