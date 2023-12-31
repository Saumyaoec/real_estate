from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model

from firebase_admin import auth
from rest_framework import authentication

from .exceptions import FirebaseError
from .exceptions import InvalidAuthToken
from .exceptions import NoAuthToken

User = get_user_model()

class FirebaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        if not auth_header:
            return (None, None)

        id_token = auth_header.split(" ").pop()
        decoded_token = None
        try:
            decoded_token = auth.verify_id_token(id_token)
        except Exception as e:
            print(e) # Error from firebase admin
            raise InvalidAuthToken("invalid-auth-token")

        if not id_token or not decoded_token:
            return (None, None)

        try:
            uid = decoded_token.get("uid")
        except Exception:
            raise FirebaseError()

        user = User.objects.get(uid=uid)
        return (user, None)