from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login, User
from rest_framework.authtoken.models import Token
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response
from datetime import datetime
from rest_framework.generics import GenericAPIView


@permission_classes((AllowAny,))
class UserLoginView(GenericAPIView):

    def get(self,request):
        context_dictionary = {}
        status_code = HTTP_200_OK
        try:
            context_dictionary['count'] = User.objects.filter(last_login__startswith=datetime.today().date()).count()
        except Exception as e:
            print("Exception occurred->", str(e))
            context_dictionary['error'] = 'An Exception occurred!!'
            status_code = HTTP_400_BAD_REQUEST
        finally:
            return Response(context_dictionary, status=status_code)

    def post(self, request):
        context_dictionary = {}
        status_code = HTTP_200_OK
        try:
            username = request.data.get("username")
            password = request.data.get("password")
            if username is None or password is None:
                context_dictionary['error'] = 'Please enter a username and a password for logging in'
                status_code = HTTP_400_BAD_REQUEST
            user = authenticate(username=username, password=password)
            if not user:
                context_dictionary['error'] = 'Incorrect username or password'
                status_code = HTTP_404_NOT_FOUND
            token, _ = Token.objects.get_or_create(user=user)
            update_last_login(None, token.user)
            context_dictionary['token'] = token.key
        except Exception as e:
            # Later, the below statement can be replaced with a " log.info "statement
            print("Exception occurred->", str(e))
            context_dictionary['error'] = 'An Exception occurred!!'
            status_code = HTTP_400_BAD_REQUEST
        finally:
            return Response(context_dictionary, status=status_code)
