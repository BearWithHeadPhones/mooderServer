from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.



class UserProfile(models.Model):
    user = models.OneToOneField(User)
    friends = models.ManyToManyField(User, related_name='friends',blank=True)
    def __str__(self):
        return "Profile of " + self.user.username


def createUserProfile(user):
    if not UserProfile.objects.filter(user=user).exists():
        userProfile = UserProfile(user=user)
        userProfile.save()



class Mood(models.Model):
    userProfile = models.ForeignKey(UserProfile)
    moodType = models.CharField(max_length=200)
    created = models.DateTimeField(default=timezone.now)
    description = models.CharField(max_length=200, blank=True)
    def __str__(self):
        return self.moodType + ":" + self.description + " " + str(self.created) + " for user " + self.userProfile.user.username