import logging
import re

from django.core.validators import ValidationError, RegexValidator
from django import forms


def validate_phone(number):
    if re.match(r'^\+\d{3} \(\d{2}\) \d{3}-\d{2}-\d{2}$', number):
        logging.log(1, 'mama')
        return number
    else:
        raise ValidationError("This field accepts mail id of google only")


class RegisterForm(forms.Form):
    user_name = forms.CharField(min_length=5, max_length=30, label="Ваше имя")
    age = forms.IntegerField(min_value=18, max_value=111, label="Ваш возраст")
    phone_number = forms.CharField(min_length=15, max_length=30, label="Ваш телефон")
    login = forms.CharField(min_length=5, max_length=30, label="Ваш логин")
    password1 = forms.CharField(label="Пароль")
    password2 = forms.CharField(min_length=3, max_length=30, label="Пароль", help_text="повторите пароль")


class LoginForm(forms.Form):
    login = forms.CharField(min_length=5, max_length=30, label="Ваш логин")
    password = forms.CharField(min_length=3, max_length=30, label="Пароль")

