from doctor.managers import (
    DailyAssessmentAbstractQuerySet,
    DaysRangeAbstractQuerySet
)
from doctor.surrounding import enums


class SurroundingDailyAssessmentQuerySet(DailyAssessmentAbstractQuerySet):

    def for_assessment(self, assessment_type):
        return self.filter(
            days_range__for_assessment=assessment_type
        )

    def remind_me_later(self):
        return self.filter(
            status=enums.REMIND_ME_LATER
        )


class SurroundingDaysRangeQuerySet(DaysRangeAbstractQuerySet):

    def total_stage_1(self):
        return self.filter(
            stage=1
        ).count()

    def for_assessment(self, assessment_type):
        return self.filter(
            for_assessment=assessment_type
        )
