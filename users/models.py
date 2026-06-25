from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    ROLE_CHOICES = [
        ('poster', 'Poster'),
        ('hunter', 'Hunter'),
    ]
    RANK_CHOICES = [
        ('novice', 'Novice'),
        ('apprentice', 'Apprentice'),
        ('expert', 'Expert'),
        ('elite', 'Elite Hunter'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='hunter')
    rank = models.CharField(max_length=15, choices=RANK_CHOICES, default='novice')
    xp = models.IntegerField(default=0)
    rating = models.FloatField(default=0.0)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"


class Badge(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='badges')
    name = models.CharField(max_length=100)
    description = models.TextField()
    earned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.profile.user.username}"
