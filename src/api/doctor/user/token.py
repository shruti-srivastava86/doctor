"""method for user tokens"""
from rest_framework.authtoken.models import Token


def delete_token(user):
    """
        Deletes an authentication token for the passed in user

        :param user: The user to delete the token for
        :type user: :class:`User <doctor.user.models.User>`
    """
    try:
        Token.objects.get(user=user).delete()
    except Token.DoesNotExist:
        pass


def regenerate_token(user):
    """
        Recreates an authentication token for the passed in user

        :param user: The user to recreate the token for
        :type user: :class:`User <doctor.user.models.User>`

        :return: The token for the user
        :rtype: Token
    """
    delete_token(user)
    return Token.objects.get_or_create(user=user)[0]


def get_token(user):
    """
        Gets an authentication token for the passed in user

        :param user: The user to get the token for
        :type user: :class:`User <doctor.user.models.User>`

        :return: The token for the user
        :rtype: Token
    """
    return Token.objects.get_or_create(user=user)[0]
