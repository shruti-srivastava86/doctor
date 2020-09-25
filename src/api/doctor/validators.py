from rest_framework.exceptions import ParseError

from doctor import enums


class Validations(object):
    @staticmethod
    def validate_status(instance, data):
        if "status" in data:
            raise ParseError(
                'You cannot edit status of the assessment.'
            )
        if not instance.status == enums.IN_PROGRESS:
            raise ParseError(
                'Your time has expired to complete your assessment.'
            )
        return data

    @staticmethod
    def validate_reopen(user, assessment_type):
        return assessment_type in user.earned_assessment_badges()
