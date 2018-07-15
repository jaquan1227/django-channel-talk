from .models import *
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url','email', 'nickname', 'created_at', 'username','password')
        extra_kwargs = {'password': {'write_only': True}}

class UserDetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'email', 'nickname', 'created_at', 'username','room_set','message_set')
        
class RoomSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Room
        fields = ('url', 'name', 'created_at', 'updated_at','user')

class RoomDetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Room
        fields = ('url', 'name', 'user', 'created_at', 'updated_at','message_set')

class MessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Message
        fields = ('url','text', 'room', 'created_at','user')

