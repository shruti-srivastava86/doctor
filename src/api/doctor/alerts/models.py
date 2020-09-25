from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _

from doctor.alerts.managers import AlertQuerySet
from doctor.models import TimestampedModel
from doctor.alerts import enums


class Alerts(TimestampedModel):
    """
        Model representing User Alerts.
    """
    objects = AlertQuerySet.as_manager()

    user = models.ForeignKey(
        'user.User',
        related_name='alerts'
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    object_id = models.PositiveIntegerField(
        blank=True,
        null=True
    )
    content_object = GenericForeignKey(
        'content_type',
        'object_id'
    )
    text = models.CharField(
        max_length=255
    )
    message = models.CharField(
        max_length=255
    )
    type = models.PositiveSmallIntegerField(
        choices=enums.ALERT_TYPE
    )
    macro_type = models.PositiveSmallIntegerField(
        choices=enums.MACRO_TYPE,
        null=True,
        blank=True
    )
    video = models.ForeignKey(
        'video.Video',
        blank=True,
        null=True
    )
    read = models.BooleanField(
        default=False
    )

    def __str__(self):
        return "{} - {}".format(self.id, self.user.email)

    class Meta:
        verbose_name = _('Alerts')
        verbose_name_plural = _('Alerts')
        ordering = ['read', '-created_at']
