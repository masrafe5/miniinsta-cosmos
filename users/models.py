from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_CONSUMER = 'consumer'
    ROLE_CREATOR  = 'creator'
    ROLE_CHOICES  = [
        (ROLE_CONSUMER, 'Consumer'),
        (ROLE_CREATOR,  'Creator'),
    ]

    role            = models.CharField(max_length=10, choices=ROLE_CHOICES, default=ROLE_CONSUMER)
    bio             = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    website         = models.URLField(blank=True)
    location        = models.CharField(max_length=150, blank=True)

    def is_creator(self):
        return self.role == self.ROLE_CREATOR

    def is_consumer(self):
        return self.role == self.ROLE_CONSUMER

    def __str__(self):
        return f'{self.username} ({self.role})'


class Follow(models.Model):
    follower  = models.ForeignKey(CustomUser, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(CustomUser, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f'{self.follower} → {self.following}'
