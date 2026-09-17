from rest_framework import serializers
from habits.models import Habit
from habits.validators import (
    RewardAndRelatedHabitValidator,
    DurationValidator,
    RelatedHabitIsPleasantValidator,
    PleasantHabitRestrictionsValidator,
    PeriodicityValidator,
)


class HabitSerializer(serializers.ModelSerializer):
    """Основной сериализатор для работы с привычками."""

    # Автоматически подставляет текущего авторизованного пользователя
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Habit
        fields = "__all__"
        # Подключаем весь комплекс созданных бизнес-валидаторов
        validators = [
            RewardAndRelatedHabitValidator(),
            DurationValidator(),
            RelatedHabitIsPleasantValidator(),
            PleasantHabitRestrictionsValidator(),
            PeriodicityValidator(),
        ]
        