
from django.contrib.auth.models import User, Group
from django.http import JsonResponse
from rest_framework import viewsets
from users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer




from rest_framework.authtoken.models import Token

def token_request(request):
        print request
        new_token = Token.objects.create(user=request.user)
        return new_token


from oauthlib.common import generate_token
from django.contrib.auth import login

from social.apps.django_app.utils import psa
from django.contrib.auth.models import User

@psa('social:complete')
def register_by_access_token(request, backend):
    # This view expects an access_token GET parameter, if it's needed,
    # request.backend and request.strategy will be loaded with the current
    # backend and strategy.
    third_party_token = request.GET.get('access_token')

    print third_party_token



    user = User.objects.get(username='bartoszcwynar')

    #user = request.backend.do_auth(third_party_token)

    if user:
        #login(request, user)

        # We get our app!
        #app = Application.objects.get(name="myapp")

        # We delete the old token
        try:
            old = Token.objects.get(user=user)
        except:
            pass
        else:
            old.delete()

        # We create a new one

        my_token = generate_token()
        # We create the access token
        # (we could create a refresh token too the same way)
        Token.objects.create(user=user,
                            key=my_token)
        print my_token

        return JsonResponse({"token": my_token})
    else:
        return "ERROR"
