from django.contrib import admin

from doctor.stop_challenge_choose.models import (
    StopChallengeChoose,
    StopChallengeChooseAssessment
)


admin.site.register(StopChallengeChoose)
admin.site.register(StopChallengeChooseAssessment)
