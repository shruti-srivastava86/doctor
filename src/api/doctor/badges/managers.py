from django.db import models

from doctor.badges import enums


class BadgeQuerySet(models.QuerySet):

    def type_macro(self):
        return self.filter(
            type__in=enums.MACRO_BADGES_TYPE
        )
