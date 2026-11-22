import os

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

from .jwt_service import JwtActivateService


class EmailService:

    @staticmethod
    def _send_email(to: str, template_name: str, context: dict, subject: str = "") -> None:
        template = get_template(template_name)
        html_content = template.render(context)
        msg = EmailMultiAlternatives(
            subject=subject,
            from_email=os.environ.get("EMAIL_HOST_USER"),
            to=[to]
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    @classmethod
    def registration_confirmation(cls, user) -> None:
        token = JwtActivateService.create_token(user)
        url = f"{os.environ.get('FRONTEND_URL')}/activate/{token}"
        cls._send_email(
            to=user.email,
            template_name="register.html",
            context={"name": user.first_name, "url": url},
            subject="Registration confirmation"
        )
