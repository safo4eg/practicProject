from django.contrib.auth.models import AbstractUser
from django.db import models

class Category(models.Model):
    title = models.CharField(max_length=25)

    def __str__(self):
        return self.title


class Application(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='uploads/%Y/%m/%d/')
    time_create = models.DateTimeField(auto_now_add=True)
    cat = models.ForeignKey(Category, on_delete=models.CASCADE)
    current_user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)

    APPLICATION_STATUS = (
        ('n', 'Новая'),
        ('a', 'Принято в работу'),
        ('c', 'Выполнено')
    )

    status = models.CharField(max_length=20, choices=APPLICATION_STATUS, default='n')

# Показ описания статуса заявки
    def show_status_message(self):
        for elem in self.APPLICATION_STATUS:
            if self.status in elem:
                application_status_message = elem[1]
                return application_status_message

class ApplicationComment(models.Model):
    APPLICATION_STATUS = (
        ('n', 'Новая'),
        ('a', 'Принято в работу'),
        ('c', 'Выполнено')
    )

    status = models.CharField(max_length=20, choices=APPLICATION_STATUS)
    image = models.ImageField(upload_to='uploads/%Y/%m/%d/', blank=True, null=True)
    description = models.TextField(blank=True)
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    time_create = models.DateTimeField(auto_now_add=True)

    def show_status_message(self):
        for elem in self.APPLICATION_STATUS:
            if self.status in elem:
                application_status_message = elem[1]
                return application_status_message




class Role(models.TextChoices):
    CUSTOMER = 'CUSTOMER', 'Клиент'
    MANAGER = 'MANAGER', 'Управляющий'

class CustomUser(AbstractUser):
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CUSTOMER)
    patronymic = models.CharField(max_length=150, verbose_name='Отчество')
    consent = models.BooleanField(blank=False, default=True)

    def get_application_amount(self):
        return self.application_set.count()


