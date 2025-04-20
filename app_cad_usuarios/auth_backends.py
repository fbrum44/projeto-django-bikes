from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend

class CPFBackend(BaseBackend):
    def authenticate(self, request, cpf=None, password=None):
        try:
            user = get_user_model().objects.get(cpf=cpf)
            if user.check_password(password):
                return user
        except get_user_model().DoesNotExist:
            return None
