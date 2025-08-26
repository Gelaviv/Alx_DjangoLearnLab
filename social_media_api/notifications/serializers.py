# notifications/serializers.py
from rest_framework import serializers
from .models import Notification
from django.contrib.auth import get_user_model

User = get_user_model()

class UserBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')

class NotificationSerializer(serializers.ModelSerializer):
    actor = UserBriefSerializer(read_only=True)
    target_object = serializers.SerializerMethodField()
    
    class Meta:
        model = Notification
        fields = ('id', 'recipient', 'actor', 'verb', 'read', 'timestamp', 'target_object')
        read_only_fields = ('id', 'recipient', 'actor', 'verb', 'timestamp', 'target_object')
    
    def get_target_object(self, obj):
        from posts.serializers import PostSerializer, CommentSerializer
        
        if obj.target:
            if hasattr(obj.target, 'title'):  # It's a Post
                return {
                    'type': 'post',
                    'data': PostSerializer(obj.target, context=self.context).data
                }
            elif hasattr(obj.target, 'content'):  # It's a Comment
                return {
                    'type': 'comment',
                    'data': CommentSerializer(obj.target, context=self.context).data
                }
        return None