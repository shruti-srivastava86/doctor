from rest_framework.exceptions import ParseError


class Validations(object):
    @staticmethod
    def validate_message(attrs):
        if not attrs.get('message'):
            raise ParseError(
                'Please provide a message for the feedback.'
            )
        return attrs
