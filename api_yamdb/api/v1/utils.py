#import uuid

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from reviews.models import User
from django.contrib.auth.tokens import default_token_generator

from api_yamdb.settings import EMAIL_ADMIN


def generate_and_send_confirmation_code_to_email(username):
    #user = get_object_or_404(User, username=username)
    user, _ = User.objects.get_or_create(email=email, username=username)
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        'Код подтвержения для завершения регистрации',
        f'Ваш код для получения JWT токена {confirmation_code}',
        EMAIL_ADMIN,
        [user.email],
        fail_silently=False,
    )
    user.save()
