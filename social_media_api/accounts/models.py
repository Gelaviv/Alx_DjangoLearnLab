# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    followers = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='following')
    
    def __str__(self):
        return self.username

    @property
    def follower_count(self):
        return self.followers.count()
    
    @property
    def following_count(self):
        return self.following.count()
    
    def is_following(self, user):
        return self.following.filter(id=user.id).exists()
    
    def follow(self, user):
        if not self.is_following(user) and self != user:
            self.following.add(user)
            return True
        return False
    
    def unfollow(self, user):
        if self.is_following(user):
            self.following.remove(user)
            return True
        return False