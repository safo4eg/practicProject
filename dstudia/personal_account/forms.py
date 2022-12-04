from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, EmailValidator
from .models import *
from .utils import *


class RegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=25, strip=True, validators=[
        RegexValidator(
            regex=r'^([а-яА-Я]|-|\s)+$',
            message='Имя должно включать только кириллицу, "-" и пробелы',
        )
    ], widget=forms.TextInput(attrs={"class": 'form-item input', "placeholder": 'Имя'}))

    last_name = forms.CharField(max_length=25, strip=True, validators=[
        RegexValidator(
            regex=r'^([а-яА-Я]|-|\s)+$',
            message='Фамилия должно включать только кириллицу, "-" и пробелы',
        )
    ], widget=forms.TextInput(attrs={"class": 'form-item input', "placeholder": 'Фамилия'}))

    patronymic = forms.CharField(max_length=25, strip=True, validators=[
        RegexValidator(
            regex=r'^([а-яА-Я]|-|\s)+$',
            message='Отчество должно включать только кириллицу, "-" и пробелы',
        )
    ], widget=forms.TextInput(attrs={"class": 'form-item input', "placeholder": 'Отчество'}))

    username = forms.CharField(max_length=15, strip=True, validators=[
        RegexValidator(
            regex=r'^([a-zA-Z]|-)+$',
            message='Логин должен включать только латиницу и "-"'
        )
    ], widget=forms.TextInput(attrs={"class": 'form-item input', "placeholder": 'Логин'}))

    email = forms.CharField(max_length=50, strip=True, validators=[
        EmailValidator(
            message='Некорректный формат email-адресса'
        )
    ], widget=forms.TextInput(attrs={"class": 'form-item input', "placeholder": 'E-mail'}))

    password = forms.CharField(max_length=125, label='Пароль',
                               widget=forms.PasswordInput(attrs={"class": 'form-item input', "placeholder": 'Пароль'}))
    repeat_password = forms.CharField(max_length=125,
                                      widget=forms.PasswordInput(attrs={"class": 'form-item input', "placeholder": 'Повторите пароль'}))
    consent = forms.BooleanField(
        label='Согласие на обработку персональных данных',
        widget=forms.CheckboxInput(attrs={"checked": True})
    )

    def save(self):
        new_user = CustomUser.objects.create(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            patronymic=self.cleaned_data['patronymic'],
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
            consent=self.cleaned_data['consent']
        )

        return new_user

    def clean(self):
        cleaned_data = super().clean()
        repeat_password = cleaned_data.get("repeat_password")
        password = cleaned_data.get('password')
        consent = cleaned_data.get('consent')

        if repeat_password != password:
            msg = 'Пароль не совпадает!'
            self.add_error('repeat_password', msg)

        if consent != True:
            msg = 'Подтвердите согласие на обработку персональных данных!'
            self.add_error('consent', msg)

        # Проверка на уникальность username:
        users = CustomUser.objects.all()
        username = cleaned_data.get('username')

        for user in users:
            if user.username == username:
                msg = 'Пользователь с таким логином уже существует!'
                self.add_error('username', msg)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=15, strip=True, label='Логин',
                               widget=forms.TextInput(attrs={"class": 'form-item input', "placeholder": 'Логин'}))
    password = forms.CharField(max_length=125, label='Пароль',
                               widget=forms.PasswordInput(attrs={"class": 'form-item input', "placeholder": 'Пароль'}))

    def clean(self):
        cleaned_date = super().clean()
        username = cleaned_date.get('username')
        password = cleaned_date.get('password')

        # Проверка на существование пользователя с логином:
        if len(CustomUser.objects.filter(username=username)) == 0:
            msg = 'Пользователь с таким логином не существует'
            self.add_error('username', msg)
        else:
            user = CustomUser.objects.get(username=username)
            if user.check_password(password) != True:
                msg = 'Неверный пароль'
                self.add_error('password', msg)


class CreateApplicationForm(forms.Form):
    title = forms.CharField(max_length=50, strip=True, widget=forms.TextInput(attrs={"class": "form-item input", "placeholder": "Название заявки"}))
    description = forms.CharField(max_length=1000, widget=forms.Textarea(attrs={"class": "form-item textarea", "placeholder": "Описание заявки"}), )
    image = forms.ImageField(label='Фото помещения/план')
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категория')


class CreateCategoryForm(forms.Form):
    title = forms.CharField(max_length=25, strip=True, label='Название', widget=forms.TextInput(attrs={"class": "form-item input", "placeholder": "Название"}))


class FilterApplicationForm(forms.Form):
    users = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(username__in=get_usernames_have_application(CustomUser.objects.all())),
        label='Пользователи',
        empty_label='Все пользователи',
        required=False
    )

    APPLICATION_STATUS = (
        ('s', 'Любой'),
        ('n', 'Новая'),
        ('a', 'Принято в работу'),
        ('c', 'Выполнено')
    )
    field = forms.ChoiceField(choices=APPLICATION_STATUS, label='Статус')


class ChangeStatusAcceptForm(forms.Form):
    description = forms.CharField(
        max_length=1000,
        widget=forms.Textarea,
        label='Добавить комментарий*'
    )


class ChangeStatusCompleteForm(forms.Form):
    description = forms.CharField(
        max_length=1000,
        widget=forms.Textarea,
        required=False,
        label='Добавить комментарий'
    )
    image = forms.ImageField(label='Прикрепить изображение*')
