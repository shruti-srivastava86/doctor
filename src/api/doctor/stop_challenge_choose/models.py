from django.db import models

from doctor.models import TimestampedModel


class StopChallengeChoose(TimestampedModel):
    """
        Model representing users Stop Challenge Choose
    """
    user = models.OneToOneField(
        'user.User',
        related_name='stop_challenge_choose'
    )
    watched_video = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Stop Challenge Choose"
        verbose_name_plural = "Stop Challenge Choose"


class StopChallengeChooseAssessment(TimestampedModel):
    """
        Model representing users Stop Challenge Choose Assessments
    """
    user = models.ForeignKey(
        'user.User',
        related_name='assessments'
    )
    stop = models.CharField(max_length=255)
    challenge = models.CharField(max_length=255)
    choose = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Assessment"
        verbose_name_plural = "Assessment"
