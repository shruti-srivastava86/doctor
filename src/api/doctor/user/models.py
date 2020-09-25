"""File creating models"""
import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import ugettext_lazy as _

from doctor.models import TimestampedModel
from doctor.user import enums
from doctor.user.managers import (
    DoctorUserManager,
    DoctorUserQueryset
)
from doctor.user.utils import profile_photo


class User(TimestampedModel, AbstractBaseUser, PermissionsMixin):
    """
        Model representing a User.
    """
    objects = DoctorUserManager()
    filter = DoctorUserQueryset.as_manager()

    name = models.CharField(
        max_length=255
    )
    email = models.EmailField(
        unique=True
    )
    gender = models.PositiveSmallIntegerField(
        choices=enums.GENDER
    )
    dob = models.DateField()
    height = models.PositiveIntegerField(
        help_text="Height in cm"
    )
    weight = models.PositiveIntegerField(
        help_text="Weight in kgs"
    )
    waist = models.PositiveIntegerField(
        help_text="Waist in cm"
    )
    photo = models.ImageField(
        upload_to=profile_photo,
        null=True,
        blank=True
    )
    one_last_thing = models.TextField(
        blank=True
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('log into django admin site.')
    )
    is_active = models.BooleanField(
        _('active'),
        default=True
    )
    best_day_streak = models.PositiveIntegerField(
        default=0
    )
    devices = models.ManyToManyField(
        'scarface.Device',
        blank=True
    )
    badges = models.ManyToManyField(
        'badges.Badges',
        blank=True
    )
    time_offset = models.IntegerField(
        default=0
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    def get_short_name(self):
        return self.name.split(" ")[0]

    def get_full_name(self):
        return self.name

    def get_username(self):
        return self.email

    def get_name_or_email(self):
        return self.name if self.name else self.email

    def earned_assessment_badges(self):
        return self.badges.type_macro().values_list(
            'type',
            flat=True
        )

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "User"
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['is_active']),
            models.Index(fields=['time_offset']),
        ]


class ForgotPassword(TimestampedModel):
    """
        Model representing a Forgot Password for a user.
    """
    user = models.ForeignKey(
        'user.User',
        related_name='forgotten_passwords'
    )
    token = models.UUIDField(
        default=uuid.uuid4,
        editable=False
    )

    def __str__(self):
        return "{} - {}".format(self.id, self.user.email)

    class Meta:
        verbose_name = _('Forgot Password')
        verbose_name_plural = _('Forgot Password')
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['token']),
        ]


class NotificationSettings(TimestampedModel):
    user = models.OneToOneField(
        'user.User',
        related_name='notification_settings'
    )
    meal = models.BooleanField(
        default=True
    )
    incomplete_day = models.BooleanField(
        default=True
    )
    good_morning = models.BooleanField(
        default=True
    )
    weekly_checkup = models.BooleanField(
        default=True
    )

    def __str__(self):
        return "{} - {}".format(self.id, self.user.email)

    class Meta:
        verbose_name = _('Notification settings')
        verbose_name_plural = _('Notification settings')
        ordering = ['id']


class GeneralSettings(TimestampedModel):
    user = models.OneToOneField(
        'user.User',
        related_name='general_settings'
    )
    alert_last_checked = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = _('General settings')
        verbose_name_plural = _('General settings')
        ordering = ['id']
