from datetime import timedelta
from typing import Union, Type

from django.contrib.auth import get_user_model
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.tokens import BlacklistMixin, Token


class ActivateToken(BlacklistMixin, Token):
    lifetime = timedelta(days=1)
    token_type = "activate"


class PasswordRecoveryToken(BlacklistMixin, Token):
    lifetime = timedelta(hours=6)
    token_type = "password_recovery"


class JwtService:
    @staticmethod
    def create_token(user, token_class: Type[Union[Token, BlacklistMixin]]):
        return token_class.for_user(user)

    @staticmethod
    def validate_token(token, token_class: Type[Union[Token, BlacklistMixin]]):
        try:
            action_token = token_class(token)
            action_token.check_blacklist()
        except Exception:
            raise InvalidToken()
        action_token.blacklist()
        user_id = action_token.payload.get("user_id")
        return get_object_or_404(get_user_model(), pk=user_id)
