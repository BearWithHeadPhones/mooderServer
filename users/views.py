from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from rest_framework import viewsets
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

@api_view(['GET'])
def getUsersMoods(request):
    #token = Token.objects.get(key=request.GET.get('access_token'))
    #print token
    #user = token.user
    userProfile = UserProfile.objects.get(user=request.user)
    moods = Mood.objects.filter(userProfile=userProfile).order_by('-created')

    print moods

    serializer = MoodSerializer(moods, many=True)
    return Response(serializer.data)



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

            print "------------------"
            print new_token
            print "-------------------"
            return JsonResponse({"token": new_token})
        else:
            return "ERROR"

    else:
        return JsonResponse({"lipa": "whuj"})
