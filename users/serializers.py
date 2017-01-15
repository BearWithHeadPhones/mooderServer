from django.contrib.auth.models import User
from models import Mood, UserProfile
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('name','username')

class MoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mood
        depth = 1
        fields = ('userProfile','moodType','created','description')