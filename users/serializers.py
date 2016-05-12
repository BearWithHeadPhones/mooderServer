from django.contrib.auth.models import User
from models import Mood
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')



class MoodSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Mood
        fields = ('moodType','created','description')