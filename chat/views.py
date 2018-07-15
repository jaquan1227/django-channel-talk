from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.permissions import *
from .permissions import *
from rest_framework.response import Response
from rest_framework import filters
from django.utils.html import mark_safe
import json
from django.shortcuts import render
from django.core.mail import EmailMessage

class UserAdminViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    def get_permissions(self):        
        permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'list':
            return UserSerializer
        return UserDetailSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = []
        else:
            permission_classes = [IsSameUser ,IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserSerializer
        return UserDetailSerializer
    def get_queryset(self):
        return User.objects.filter(username=self.request.user.username)

    # def perform_create(self, serializer):
    #     print(self.request.body)
    #     serializer.save(user=self.request.user)
        
class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ['name']
    def get_permissions(self):
        if self.action == 'list' or self.action == 'create':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsRoomMember]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action =='retrieve':
            return RoomDetailSerializer
        return RoomSerializer

    def get_queryset(self):
        return self.request.user.room_set
    
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (IsOwner,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ['text']
    def get_queryset(self):
        return self.request.user.message_set

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsOwner]
        return [permission() for permission in permission_classes]

def index(request):
    return render(request, 'chat/index.html', {})

def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })
