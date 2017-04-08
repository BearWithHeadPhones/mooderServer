from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from users.serializers import UserSerializer, MoodSerializer
from users.models import Mood,UserProfile
from django.utils import timezone
import operator


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

@api_view(['GET','POST'])
def getTimelineEntriesFriends(request):

    if request.method == 'GET':

        userProfile = UserProfile.objects.get(user=request.user)
        length = int(request.GET.get('length'))
        print length
        moods = []
        moods += Mood.objects.filter(userProfile=userProfile)
        for friend in userProfile.friends.all():
            print friend
            friendProfile = UserProfile.objects.get(user=friend)
            moods += Mood.objects.filter(userProfile=friendProfile)

        moods = sorted(moods, key=operator.attrgetter('created'), reverse=True)

        moods = moods[:length*10]
        print moods
        serializer = MoodSerializer(moods, many=True)
        print serializer.data
        return Response(serializer.data)
    elif request.method == 'POST':
        print "siemacha"
        print request.user
        print request.data
        print request.data.get("moodType")
        print request.data.get("description")

        Mood.objects.create(userProfile = UserProfile.objects.get(user=request.user), moodType =request.data.get("moodType"),created= timezone.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), description=request.data.get("description"))
        return Response(request.data, status=status.HTTP_201_CREATED)








from oauthlib.common import generate_token
from social.apps.django_app.utils import psa
from helpers import facebookHelper
import models



@psa('social:complete')
def register_by_access_token(request, backend):
    # This view expects an access_token GET parameter, if it's needed,
    # request.backend and request.strategy will be loaded with the current
    # backend and strategy.

    print "siema"
    if facebookHelper.validateUserByToken(request.GET.get('access_token')):
        try:
            user = User.objects.get(username=request.GET.get('USER'))
        except:
            user = User.objects.create_user(request.GET.get('USER'))
            models.createUserProfile(user)
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
            userProfile.name = facebookHelper.getUserById(request.GET.get('access_token'),user)["name"]
            print 'USERNAME:' + user.username
            userProfile.username = user.username
            userProfile.save()
            for friend in facebookHelper.getUsersFriends(request.GET.get('access_token'),user):
                try:
                    userProfile.friends.add(User.objects.get(username = friend["id"]))
                except:
                    pass


            return JsonResponse({"token": new_token})
        else:
            return "ERROR"

    else:
        return JsonResponse(status.HTTP_401_UNAUTHORIZED)
