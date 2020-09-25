from django.utils import timezone

from rest_framework.exceptions import ParseError


class Validations(object):
    @staticmethod
    def validate_meal(daily_assessment, data):
        if not data:
            raise ParseError(
                'Please provide a meal.'
            )
        meal_object = daily_assessment.meals.filter(
                id=data.get('id')
        ).first()
        if not meal_object:
            raise ParseError(
                'Invalid assessment meal id provided.'
            )
        return meal_object

    @staticmethod
    def validate_weekly_log(weekly_assessment, data):
        if weekly_assessment.bmi or weekly_assessment.waist:
            raise ParseError(
                'You have already completed your weekly checkup.'
            )
        if timezone.now().date() > weekly_assessment.created_at.date():
            raise ParseError(
                'Your time has expired to complete your weekly checkup.'
            )
        if not data.get('bmi'):
            raise ParseError(
                'Please provide a bmi value.'
            )
        if not data.get('waist'):
            raise ParseError(
                'Please provide a waist circumference value.'
            )
        return data
