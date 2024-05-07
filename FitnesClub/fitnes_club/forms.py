import logging
import re

from django.core.validators import ValidationError
from django import forms


class RegisterForm(forms.Form):
    user_name = forms.CharField(min_length=1, max_length=30, label="Ваше имя")
    age = forms.IntegerField(min_value=18, max_value=111, label="Ваш возраст")
    phone_number = forms.CharField(min_length=15, max_length=30, label="Ваш телефон")
    login = forms.CharField(min_length=1, max_length=30, label="Ваш логин")
    password1 = forms.CharField(label="Пароль")
    password2 = forms.CharField(min_length=3, max_length=30, label="Пароль", help_text="повторите пароль")


class LoginForm(forms.Form):
    login = forms.CharField(min_length=1, max_length=30, label="Ваш логин")
    password = forms.CharField(min_length=3, max_length=30, label="Пароль")


class FilterForm(forms.Form):
    category = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices={"Category1": "Category1", "Category2": "Category2", "Category3": "Category3"},
    )
    max_price = forms.IntegerField(min_value=1, required=False)


def validate_phone(number):
    if not re.fullmatch(r'^\+\d{3} \(\d{2}\) \d{3}-\d{2}-\d{2}$', number):
        raise ValidationError("Номер должен соответствовать формату: +375 (XX) XXX-XX-XX")


class InstructorForm(forms.Form):
    fullname = forms.CharField(max_length=100)
    age = forms.IntegerField(min_value=18, max_value=111)
    phone_number = forms.CharField(max_length=30, validators=[validate_phone])
    about = forms.CharField()
    photo = forms.ImageField(required=False)
    old_password = forms.CharField(required=False, label="Введите старый пароль",
                                   help_text="Для изменения логина и пароля данное поле является обязательным")
    login = forms.CharField()
    password1 = forms.CharField(required=False, label="Новый пароль")
    password2 = forms.CharField(required=False, label="Подтвердите пароль")


class ClientForm(forms.Form):
    fullname = forms.CharField(max_length=100)
    age = forms.IntegerField(min_value=18, max_value=111)
    phone_number = forms.CharField(max_length=30, validators=[validate_phone])
    login = forms.CharField()
    old_password = forms.CharField(required=False, label="Введите старый пароль",
                                   help_text="Для изменения логина и пароля данное поле является обязательным")
    password1 = forms.CharField(required=False, label="Новый пароль")
    password2 = forms.CharField(required=False, label="Подтвердите пароль")

    def clean(self):
        old_password = self.cleaned_data.get('old_password')
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if old_password:
            if not password1:
                self.add_error('password1', "Введите новый пароль")
            if password1 != password2:
                self.add_error('password2', "Пароли не совпадают!")

