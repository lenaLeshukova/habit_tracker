from rest_framework.exceptions import ValidationError


class RewardAndRelatedHabitValidator:
    """Исключает одновременный выбор связанной привычки и указания вознаграждения."""

    def __call__(self, attrs):
        reward = attrs.get("reward")
        related_habit = attrs.get("related_habit")

        if reward and related_habit:
            raise ValidationError(
                "Нельзя одновременно заполнять поле вознаграждения и связанной привычки. "
                "Выберите что-то одно."
            )


class DurationValidator:
    """Проверяет, что время выполнения привычки составляет не более 120 секунд."""

    def __call__(self, attrs):
        duration = attrs.get("duration")

        if duration and duration > 120:
            raise ValidationError(
                "Время выполнения привычки не должно превышать 120 секунд (2 минуты)."
            )


class RelatedHabitIsPleasantValidator:
    """Проверяет, что в связанные привычки попадают только привычки с признаком приятной."""

    def __call__(self, attrs):
        related_habit = attrs.get("related_habit")

        if related_habit and not related_habit.is_pleasant:
            raise ValidationError(
                "В качестве связанной привычки можно выбрать только ту привычку, "
                "у которой установлен признак приятной (is_pleasant=True)."
            )


class PleasantHabitRestrictionsValidator:
    """У приятной привычки не может быть вознаграждения или связанной привычки."""

    def __call__(self, attrs):
        is_pleasant = attrs.get("is_pleasant", False)
        reward = attrs.get("reward")
        related_habit = attrs.get("related_habit")

        if is_pleasant:
            if reward or related_habit:
                raise ValidationError(
                    "У приятной привычки не может быть вознаграждения или связанной привычки."
                )


class PeriodicityValidator:
    """Проверяет, что периодичность выполнения привычки составляет не реже, чем 1 раз в 7 дней."""

    def __call__(self, attrs):
        # Если поле не передано (например, при PATCH запросе), валидацию пропускаем
        if "periodicity" in attrs:
            periodicity = attrs.get("periodicity")

            if periodicity is None or periodicity > 7 or periodicity < 1:
                raise ValidationError(
                    "Нельзя выполнять привычку реже, чем 1 раз в 7 дней (значение должно быть от 1 до 7)."
                )
            