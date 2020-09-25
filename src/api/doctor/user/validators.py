import re

from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.exceptions import ParseError

from doctor.badges import enums
from doctor.user.models import User


class Validations(object):
    @staticmethod
    def validate_email(obj):
        if not obj:
            raise serializers.ValidationError("Email can't be empty")
        elif User.objects.filter(email=obj.lower()):
            raise serializers.ValidationError(
                "User with this email already exists"
            )
        return obj.lower()

    @staticmethod
    def validate_valid_email(obj):
        if not obj:
            raise serializers.ValidationError("Email can't be empty")
        return obj.lower()

    @staticmethod
    def validate_password(obj):
        pattern = re.compile(r'^(?=.*[a-z])(?=.*\d)(?=.*[A-Z])(?:.{8,})$')
        if not pattern.match(obj):
            raise serializers.ValidationError(
                "Password should contain Min. 8 characters, "
                "including at least one UPPERCASE "
                "and lowercase character and at least one number."
            )
        return obj

    @staticmethod
    def validate_login(data):
        email = data.get('email')
        password = data.get('password')
        user = authenticate(username=email, password=password)
        if not user:
            raise ParseError(
                _('Incorrect email address and password combination.')
            )
        data['user'] = user
        return data

    @staticmethod
    def validate_change_password(instance, data):
        old_password = data.get("old_password")
        password = data.get("password")
        is_correct_password = instance.check_password(old_password)
        if old_password is None or password is None:
            raise ParseError(
                _("You must provide your old and new password.")
            )
        elif not is_correct_password:
            raise ParseError(
                _("Your old password is incorrect.")
            )
        elif old_password == password:
            raise ParseError(
                _("Please enter a password different from your current one.")
            )
        elif len(password) < 8:
            raise ParseError(
                _("Min. 8 characters, including at least one UPPERCASE "
                  "and lowercase character and at least one number.")
            )
        return data

    @staticmethod
    def validate_badges(data):
        for badge in data:
            if badge.type not in [enums.SHARING, enums.INFLUENCER]:
                raise serializers.ValidationError(
                    _("Invalid badge type")
                )
        return data
