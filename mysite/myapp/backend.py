from django.apps import apps
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured

import logging

# import the custom User object
from .models import V2OfUsers


# Name my backend 'V2OfBackend'
class V2OfBackend(object):
    """
    Authenticate against the table V2OfUsers.

    Use the login name, and a password.
    """

    # Create an authentication method
    # This is called by the standard Django login procedure
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Try to find a user matching your username in CUSTOM_USER_MODEL
        userC = self.user_class.objects.get(username__exact=username)
        login_valid = (userC.username == username)
        pwd_valid = (userC.password == password)
        if login_valid and pwd_valid:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                # No user was found, so add him
                user = User(
                    username = username,
                    email = userC.email,
                    first_name = userC.firstname,
                    last_name = userC.lastname,
                    is_active = userC.is_active,
                )
                user.set_password(password)
                user.is_staff = False
                user.is_superuser = False
                user.save()
            except Exception as e:
                logging.getLogger("error_logger").error(repr(e))
            return user
        return None


    # Required for backend to work properly - unchanged in most scenarios
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


    # Required to select auth model defined in settings.py
    @property
    def user_class(self):
        if not hasattr(self, '_user_class'):
            self._user_class = apps.get_model(*settings.CUSTOM_USER_MODEL.split('.', 2))
            if not self._user_class:
                raise ImproperlyConfigured('Could not get custom user model')
        return self._user_class
