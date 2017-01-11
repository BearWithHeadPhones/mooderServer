from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from users.serializers import UserSerializer, MoodSerializer
from users.models import Mood,UserProfile


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

@api_view(['GET','POST'])
def getUsersMoods(request):

    if request.method == 'GET':

        userProfile = UserProfile.objects.get(user=request.user)
        #moods = Mood.objects.filter(userProfile=userProfile).order_by('-created')
        moods = []
        for friend in userProfile.friends.all():
            print friend
            friendProfile = UserProfile.objects.get(user=friend)
            moods += Mood.objects.filter(userProfile=friendProfile).order_by('-created')

        print moods
        serializer = MoodSerializer(moods, many=True)
        print serializer.data
        return Response(serializer.data)
    elif request.method == 'POST':
        print "siemacha"
        print request.user
        print request.data.get("moodType")

        Mood.objects.create(userProfile = UserProfile.objects.get(user=request.user), moodType =request.data.get("moodType"))
        return Response(request.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def updateUsersFriends(request):

    if request.method == 'GET':
        print facebookHelper.getUsersFriends(request.GET.get('access_token'),request.user)
        return Response(request.data, status=status.HTTP_200_OK)






from oauthlib.common import generate_token
from social.apps.django_app.utils import psa
from helpers import facebookHelper
import models



@psa('social:complete')
def register_by_access_token(request, backend):
    # This view expects an access_token GET parameter, if it's needed,
    # request.backend and request.strategy will be loaded with the current
    # backend and strategy.

    if facebookHelper.validateUserByToken(request.GET.get('access_token')):
        try:
            user  = User.objects.get(username=request.GET.get('USER'))
        except:
            user = User.objects.create_user(request.GET.get('USER'))
            models.createUserProfile(user)
            print
        if user:
            try:
                old = Token.objects.get(user=user)
            except:
                pass
            else:
                old.delete()

            new_token = generate_token()

            Token.objects.create(user=user,
                                key=new_token)

            print "friends"

            userProfile = UserProfile.objects.get(user=user)

            for friend in facebookHelper.getUsersFriends(request.GET.get('access_token'),user):
                print friend["id"]
                userProfile.friends.add(User.objects.get(username = friend["id"]))

            return JsonResponse({"token": new_token})
        else:
            return "ERROR"

    else:
        return JsonResponse(status.HTTP_401_UNAUTHORIZED)
