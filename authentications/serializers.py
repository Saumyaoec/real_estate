from rest_framework import serializers
from .models import *

from django.utils.translation import gettext_lazy as _



class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "contact",
            "country_code",
            "country",
            "first_name",
            "last_name",
        ]
        extra_kwargs = {
            "password": {"write_only": True, "required": True},
            "email": {"required": True},
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    def create(self, validated_data):
        email = validated_data.pop("email")
        password = validated_data.pop("password")
        user = User.objects.create_user(email, password)

        user.contact = validated_data["contact"]
        user.country = validated_data["country"]
        user.first_name = validated_data["first_name"]
        user.last_name = validated_data["last_name"]
        user.country_code = validated_data["country_code"]
        user.save()
        return user




class UserAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "uid",
            "email",
            "country",
            "country_code",
            "contact",
        ]
        read_only_fields = ("__all__",)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        if email and password:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                msg = _("User not registered.")
                raise serializers.ValidationError(msg, code="authorization")
            data["user"] = user
            return data
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code="authorization")


class AdminLoginSerializer(LoginSerializer):
    def validate(self, data):
        user = super().validate(data)
        if not user.is_superuser or not user.is_staff:
            msg = _("User does not have sufficient privileges to log in.")
            raise serializers.ValidationError(msg, code="authorization")
        return user


