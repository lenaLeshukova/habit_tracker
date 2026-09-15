from django.conf import settings
from django.db import models


class Habit(models.Model):
    """Модель привычки для трекера."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="habits",
        verbose_name="Создатель привычки",
    )
    place = models.CharField(
        max_length=255,
        verbose_name="Место выполнения",
        help_text="Где необходимо выполнять привычку",
    )
    time = models.TimeField(
        verbose_name="Время выполнения",
        help_text="Когда необходимо выполнять привычку",
    )
    action = models.CharField(
        max_length=255,
        verbose_name="Действие",
        help_text="Что представляет собой привычка",
    )
    is_pleasant = models.BooleanField(
        default=False,
        verbose_name="Признак приятной привычки",
        help_text="Поставьте галочку, если это приятная привычка-вознаграждение",
    )
    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="useful_habits",
        verbose_name="Связанная привычка",
        help_text="Приятная привычка, которая связана с полезной привычкой",
    )
    periodicity = models.PositiveIntegerField(
        default=1,
        verbose_name="Периодичность (в днях)",
        help_text="Как часто выполнять привычку (например: 1 — каждый день, 7 — раз в неделю)",
    )
    reward = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Вознаграждение",
        help_text="Чем пользователь себя вознаградит после выполнения",
    )
    duration = models.PositiveIntegerField(
        default=60,
        verbose_name="Время на выполнение (в секундах)",
        help_text="Сколько времени займет выполнение привычки (не более 120 секунд)",
    )
    is_public = models.BooleanField(
        default=False,
        verbose_name="Признак публичности",
        help_text="Видна ли эта привычка другим пользователям в общем списке",
    )

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = ["id"]

    def __str__(self):
        return f"Я буду {self.action} в {self.time} в {self.place}"
