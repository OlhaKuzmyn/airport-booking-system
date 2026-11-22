from datetime import timedelta

from django.contrib.auth import get_user_model
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.tokens import BlacklistMixin, Token


class ActivateToken(BlacklistMixin, Token):
    lifetime = timedelta(days=1)
    token_type = "activate"


class JwtActivateService:
    @staticmethod
    def create_token(user):
        return ActivateToken.for_user(user)

    @staticmethod
    def validate_token(token):
        try:
            action_token = ActivateToken(token)
            action_token.check_blacklist()
        except Exception:
            raise InvalidToken()
        action_token.blacklist()
        user_id = action_token.payload.get("user_id")
        return get_object_or_404(get_user_model(), pk=user_id)
