# posts/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import  FeedView


router = DefaultRouter()
router.register(r'posts', views.PostViewSet)
router.register(r'comments', views.CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),

    path('posts/<int:pk>/like/', views.PostViewSet.as_view({'post': 'like'}), name='post-like'),
    path('posts/<int:pk>/unlike/', views.PostViewSet.as_view({'post': 'unlike'}), name='post-unlike'),
    path('feed/', FeedView.as_view(), name='feed'),
    
]