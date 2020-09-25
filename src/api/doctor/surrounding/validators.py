from rest_framework.exceptions import ParseError

from doctor import enums
from doctor.surrounding import enums as surrounding_enums


class Validations(object):
    @staticmethod
    def validate_status(instance, attrs):
        status = attrs.get('status')
        if not status:
            raise ParseError(
                'Please provide a status.'
            )
        if status not in [enums.COMPLETE,
                          surrounding_enums.CANNOT_DO_IT,
                          surrounding_enums.REMIND_ME_LATER]:
            raise ParseError(
                'Please provide a valid status.'
            )
        if not instance.status == enums.IN_PROGRESS:
            raise ParseError(
                'Your time has expired to complete your assessment.'
            )
        return attrs
