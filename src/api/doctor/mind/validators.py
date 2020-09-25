from rest_framework.exceptions import ParseError


class Validations(object):
    @staticmethod
    def validate_identify(identify, day):
        if not identify and day > 21:
            raise ParseError(
                'Please provide why did you stop at this moment.'
            )

    @staticmethod
    def validate_choose(choose, day):
        if not choose and day > 44:
            raise ParseError(
                'Please provide why did you choose to action this.'
            )
