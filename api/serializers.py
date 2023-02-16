from dataclasses import field
from rest_framework import  serializers
from rest_framework.permissions import IsAuthenticated
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from . import models as api_models

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name',
                  'email', 'avatar', 'password','username')
        extra_kwargs = {
            'password': {'write_only': True, 'required': False}
        }




class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = api_models.Conversation
        exclude = ('created_at', 'updated_at','created_by')

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = api_models.Message
        exclude=('linked_conversation','updated_at','creator',)


class api_user_serializer(serializers.ModelSerializer):
    class Meta:
        model = api_models.User
        exclude =('password','id','groups','user_permissions','is_superuser','is_staff','is_active','last_login','date_joined')
        
        
class CallSerializer(serializers.ModelSerializer):
    class Meta:
        model=api_models.Call
        field="__all__"
