from django.db import models
from django.utils.translation import ugettext_lazy as _

from doctor.models import TimestampedModel
from doctor.video import enums
from doctor.video.managers import VideoQuerySet
from doctor.video.utils import alert_video


class Video(TimestampedModel):
    """
        Model representing Videos.
    """
    objects = VideoQuerySet.as_manager()

    file = models.FileField(
        upload_to=alert_video,
        null=True,
        blank=True
    )
    type = models.PositiveSmallIntegerField(
        choices=enums.VIDEO_TYPES,
        unique=True
    )

    class Meta:
        verbose_name = _('Video')
        verbose_name_plural = _('Video')
        ordering = ['type']
