from django.db import models
from django.utils.translation import ugettext_lazy as _

from doctor.badges import enums
from doctor.badges.managers import BadgeQuerySet
from doctor.models import TimestampedModel


class Badges(TimestampedModel):
    """
        Model representing Badges.
    """
    objects = BadgeQuerySet.as_manager()

    name = models.CharField(
        max_length=255
    )
    description = models.TextField(
        null=True,
        blank=True
    )
    type = models.SmallIntegerField(
        choices=enums.BADGES,
        unique=True
    )

    def __str__(self):
        return "{} - {} - {}".format(self.id, self.name, self.type)

    class Meta:
        verbose_name = _('Badges')
        verbose_name_plural = _('Badges')
        ordering = ['type']
