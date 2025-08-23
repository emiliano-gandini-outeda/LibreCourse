from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class EmailUsernameBackend(ModelBackend):
    def authenticate(self, request, username=None, email=None, password=None, **kwargs):
        if email is None or username is None:
            return None
        try:
            user = UserModel.objects.get(email__iexact=email, username=username)
        except UserModel.DoesNotExist:
            return None

        if user.check_password(password):
            return user
        return None
