from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings
from django.utils import timezone


class Client(models.Model):
    email = models.EmailField(unique = True, verbose_name = "Электронная почта")
    full_name =models.CharField(max_length = 150, verbose_name = "ФИО")
    comment = models.TextField(blank = True, null = True, verbose_name = "Комментарии")

    owner = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete =models.CASCADE,
                             blank = True, null = True, verbose_name = "Владелец")
    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    def __str__(self):
        return f"{self.full_name} ({self.email})"

class Message(models.Model):
    theme = models.CharField(unique = True,max_length = 100, verbose_name = "Тема письма")
    body = models.TextField(blank = True, null = True, verbose_name = "Тело письма")

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE,
                              blank = True, null = True, verbose_name = "Владелец" )

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"

    def __str__(self):
        return f"{self.theme} ({self.owner})"


class Mailing (models.Model):
    start_time = models.DateTimeField( verbose_name = "Дата и время начала")
    end_time = models.DateTimeField( verbose_name = "Дата и время окончания")

    message = models.ForeignKey('Message', on_delete = models.CASCADE,
                                blank = True, null = True, verbose_name = "Сообщение")
    recipients = models.ManyToManyField('Client',
                                blank = True, verbose_name = "Получатель")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete = models.CASCADE,
                                blank = True, null = True, verbose_name = "Владелец")

    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('started', 'Запущена'),
        ('completed', 'Завершена'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='created')

    def clean(self):

        super().clean()

        if self.start_time and self.end_time:

            if self.end_time <= self.start_time:
                raise ValidationError({
                    'end_time': "Дата окончания не может быть раньше или равна дате начала."
                })

            if not self.pk and self.start_time < timezone.now():
                raise ValidationError({
                    'start_time': "Рассылка не может начинаться в прошлом."
                })


