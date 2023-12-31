import requests
from rest_framework import status
from requests.exceptions import HTTPError
from rest_framework.exceptions import APIException


def raise_detailed_error_firebase(request_object):
    try:
        request_object.raise_for_status()
    except requests.exceptions.RequestException as err:
        print(err)
        if request_object.json()["error"]["message"]:
            raise FirebaseError(request_object.json()["error"]["message"])
        raise HTTPError(err)


class InvalidCoupon(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = "invalid_coupon"
    default_detail = "Invalid coupon"


class NoAuthToken(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "no-auth-tkn"
    default_code = "no_auth_token"


class InvalidAuthToken(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "invalid-auth-tkn-given"
    default_code = "invalid_token"


class FirebaseError(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "not-valid-fb-user"
    default_code = "no_firebase_uid"


class EmailAlreadyExist(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "email-exists"
    default_code = "email_exists"


class UserNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "user-not-found"
    default_code = "user_not_found"