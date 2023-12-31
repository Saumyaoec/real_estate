import json
import requests
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, BaseUserManager

from .exceptions import *

# firebase


class UserManager(BaseUserManager):
    def create_user(self, email, password):
        """
        Creates and saves a User with the given email, username and password.
        """
        if not (email and password):
            raise ValueError("Email address and password is required")

        user_data = self.create_user_with_email_and_password(email, password)
        uid = user_data["localId"]
        user = self.model(email=self.normalize_email(email), username=email, uid=uid)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        """
        Creates and saves a superuser with the given email, username and password.
        """
        user = self.create_user(
            email,
            password=password,
        )

        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def create_user_with_email_and_password(self, email, password):
        request_ref = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/signupNewUser?key={0}".format(
            settings.FIREBASE_API_KEY
        )
        headers = {"content-type": "application/json; charset=UTF-8"}
        data = json.dumps(
            {"email": email, "password": password, "returnSecureToken": True}
        )
        request_object = requests.post(request_ref, headers=headers, data=data)
        raise_detailed_error_firebase(request_object)
        return request_object.json()


class User(AbstractUser):
    uid = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(unique=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    country_code = models.CharField(max_length=10, null=True, blank=True)
    contact = models.CharField(max_length=15, null=True, blank=True, unique=True)
    time_zone = models.CharField("Timezone name", max_length=10, default="UTC")
    photo = models.FileField(
        "Profile picture", upload_to="user/%Y/%m/", blank=True, null=True, default=None
    )
    rec_by = models.ForeignKey(
        "User",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="referred_by_users",
    )
    active = models.BooleanField(default=True)
    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email

    def sign_in_with_email_and_password(self, email, password):
        request_ref = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key={0}".format(
            settings.FIREBASE_API_KEY
        )
        headers = {"content-type": "application/json; charset=UTF-8"}
        data = json.dumps(
            {"email": email, "password": password, "returnSecureToken": True}
        )
        request_object = requests.post(request_ref, headers=headers, data=data)
        raise_detailed_error_firebase(request_object)
        self.last_login = timezone.now()
        self.save()
        return request_object.json()

    