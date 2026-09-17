from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """Менеджер для кастомной модели пользователя, где email является уникальным идентификатором."""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Поле Email должно быть заполнено')
        email = self.normalize_email(email)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Кастомная модель пользователя для трекера привычек."""

    # Убираем поле username
    username = None

    email = models.EmailField(
        unique=True,
        verbose_name='Email адрес',
        help_text='Используется в качестве логина'
    )

    # Дополнительные поля (опционально, для удобства работы с Telegram)
    telegram_chat_id = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Telegram Chat ID',
        help_text='ID чата в Telegram для отправки уведомлений'
    )
    avatar = models.ImageField(
        upload_to='users/avatars/',
        blank=True,
        null=True,
        verbose_name='Аватар'
    )

    # Настройки авторизации
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Теперь при create_superuser будет запрашиваться только email и password

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email
