from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password = None, **extra_fields):
        if not email:
            raise ValueError("Email must be set")
        email = self.normalize_email(email)
        user = self.model(email = email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user



class Useпшr(AbstractUser):
    username = None
    email = models.EmailField(unique = True, verbose_name = "Электронная почта")
    avatar = models.ImageField(upload_to = "users/avatars/", blank = True, null = True, verbose_name = "Аватар")
    phone_number = models.CharField(max_length = 100, blank = True, null = True, verbose_name = "Номер телефона")
    country = models.CharField(max_length = 100, blank = True, null = True, verbose_name = "Страна")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

        def __str__(self):
            return self.email

