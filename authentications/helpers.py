from firebase_admin import auth
from django.contrib.auth import get_user_model

from .exceptions import *

User = get_user_model()


# Helper function to verify Firebase ID token
def verify_firebase_id_token(id_token):
    try:
        return auth.verify_id_token(id_token)
    except Exception as e:
        print(e)  # Error from Firebase admin
        raise InvalidAuthToken("invalid-auth-token")


# Helper function to get user by UID
def get_user_by_uid(uid):
    try:
        return User.objects.get(uid=uid)
    except User.DoesNotExist:
        raise UserNotFound("user not found")


# Common function to get user by ID token
def get_user_by_id_token(id_token):
    decoded_token = verify_firebase_id_token(id_token)
    uid = decoded_token.get("uid")
    return get_user_by_uid(uid)


# Common function to get UID from request
def get_uid_from_request(request):
    auth_header = request.META.get("HTTP_AUTHORIZATION")
    if not auth_header:
        raise NoAuthToken("no-auth-token")
    id_token = auth_header.split(" ").pop()
    decoded_token = verify_firebase_id_token(id_token)
    uid = decoded_token.get("uid")
    return uid