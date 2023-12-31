from rest_framework.permissions import BasePermission

from .helpers import get_uid_from_request, get_user_by_uid
from .exceptions import InvalidAuthToken, NoAuthToken, UserNotFound


class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        try:
            get_uid_from_request(request)
            return True
        except (NoAuthToken, InvalidAuthToken):
            return False


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        try:
            uid = get_uid_from_request(request)
            user = get_user_by_uid(uid)
            return user.is_staff and user.is_active
        except (NoAuthToken, InvalidAuthToken, UserNotFound):
            return False
        

class IsOwnerOrStaff(BasePermission):
    message = "permission-denied"

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True

        if hasattr(obj, "user"):
            return obj.user == request.user

        return False