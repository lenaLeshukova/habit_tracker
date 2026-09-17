from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from habits.models import Habit
from habits.serializers import HabitSerializer
from habits.permissions import IsOwner


class HabitViewSet(viewsets.ModelViewSet):
    """
    ViewSet для CRUD операций над привычками текущего пользователя.
    """
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        # Пользователь видит только свои привычки
        # Проверка на авторизацию сработает раньше благодаря IsAuthenticated
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Сохраняем привычку, привязывая её к текущему пользователю
        serializer.save(user=self.request.user)


class PublicHabitListAPIView(generics.ListAPIView):
    """
    Эндпоинт для просмотра списка всех публичных привычек.
    Доступен всем пользователям (даже неавторизованным, если нужно, либо IsAuthenticated).
    без возможности редактирования или удаления.
    """
    queryset = Habit.objects.filter(is_public=True)
    serializer_class = HabitSerializer
    permission_classes = [AllowAny]  # Или IsAuthenticated, если просмотр только для вошедших
