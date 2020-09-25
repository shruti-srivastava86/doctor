from django.db import models

from doctor.video import enums


class VideoQuerySet(models.QuerySet):

    def welcome(self):
        return self.filter(
            type=enums.WELCOME
        ).first()

    def weight_installation(self):
        return self.filter(
            type=enums.WEIGHT_INSTALLATION
        ).first()

    def food_and_hydration_installation(self):
        return self.filter(
            type=enums.FOOD_AND_HYDRATION_INSTALLATION
        ).first()

    def motion_installation(self):
        return self.filter(
            type=enums.MOTION_INSTALLATION
        ).first()

    def sleep_installation(self):
        return self.filter(
            type=enums.SLEEP_INSTALLATION
        ).first()

    def mind_installation(self):
        return self.filter(
            type=enums.MIND_INSTALLATION
        ).first()

    def stop_challenge_choose_welcome(self):
        return self.filter(
            type=enums.STOP_CHALLENGE_CHOOSE
        ).first()

    def missing_a_day(self):
        return self.filter(
            type=enums.MISSING_A_DAY
        ).first()

    def failing_a_macro(self):
        return self.filter(
            type=enums.FAILING_A_MACRO
        ).first()
