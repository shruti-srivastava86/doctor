from django.db import models

from doctor.models import TimestampedModel


class Feedback(TimestampedModel):
    user = models.ForeignKey(
        'user.User',
        related_name='feedback'
    )
    message = models.TextField()

    class Meta:
        verbose_name = "Feedback"
        verbose_name_plural = "Feedback"
        ordering = ['-created_at']
