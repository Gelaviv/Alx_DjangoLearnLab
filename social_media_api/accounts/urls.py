# accounts/urls.py
from django.urls import path
from . import views



urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.user_login, name='login'),
    # path('logout/', views.user_logout, name='logout'),
    path('profile/', views.user_profile, name='profile'),
    # path('users/', views.user_list, name='user-list'),
    path('follow/', views.follow_user, name='follow-user'),
    path('unfollow/', views.unfollow_user, name='unfollow-user'),
    path('following/', views.following_list, name='following-list'),
    path('followers/', views.followers_list, name='followers-list'),

]