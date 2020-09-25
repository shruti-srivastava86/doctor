from rest_framework.exceptions import ParseError


class Validations(object):
    @staticmethod
    def validate_sleep(sleep_type):
        if not sleep_type:
            raise ParseError(
                'Please provide sleep type.'
            )
