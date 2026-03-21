from django.db import models
from django.conf import settings



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


