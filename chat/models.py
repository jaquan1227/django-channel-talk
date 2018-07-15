from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.hashers import make_password, is_password_usable

class User(AbstractUser):
    email = models.EmailField(
        verbose_name='Email address',
        max_length=255,
        unique=True,
    )
    nickname = models.CharField(
        verbose_name='Nickname',
        max_length=30,
        unique=True
    )
    username = models.CharField(
        verbose_name='UserName',
        max_length=30,
        unique=True
    )
    created_at = models.DateTimeField(
        verbose_name='Create Date',
        default=timezone.now
    )

    class Meta:
        verbose_name = ('user')
        verbose_name_plural = ('users')
        ordering = ('-created_at',)

    def __str__(self):
        return self.nickname
    
@receiver(pre_save, sender=User)
def password_hashing(instance, **kwargs):
    if not is_password_usable(instance.password):
        instance.password = make_password(instance.password)

class Room(models.Model):
    name = models.CharField(
        verbose_name='RoomName',
        max_length=100
    )
    user = models.ManyToManyField(
        User,
        verbose_name='RoomUser'
    )
    created_at = models.DateTimeField(
        verbose_name='Create Date',
        default=timezone.now
    )
    updated_at = models.DateTimeField(
        verbose_name='Update date',
        default=timezone.now,
        null= True
    )
    class Meta:
        ordering = ('-updated_at',)

    def __str__(self):
        return self.name

class Message(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='MessageUser'
    )
    room = models.ForeignKey(
        Room, on_delete=models.CASCADE,
        verbose_name='MessageRoom'
    )
    text = models.TextField()

    created_at = models.DateTimeField(
        verbose_name='Create Date',
        default=timezone.now
    )
    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.text