from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from habits.models import Habit


class HabitAPITests(APITestCase):
    """Комплексные тесты для API привычек и валидаторов."""

    def setUp(self):
        # Создаем двух пользователей для проверки прав доступа
        self.user1 = User.objects.create_user(
            email="owner@example.com", password="password123"
        )
        self.user2 = User.objects.create_user(
            email="other@example.com", password="password123"
        )

        # Создаем базовую приятную привычку (будет использоваться как связанная)
        self.pleasant_habit = Habit.objects.create(
            user=self.user1,
            place="Дом",
            time="08:00:00",
            action="Принять пенную ванну",
            is_pleasant=True,
        )

        # Создаем обычную полезную привычку для user1
        self.habit = Habit.objects.create(
            user=self.user1,
            place="Парк",
            time="07:00:00",
            action="Бег",
            duration=60,
            periodicity=1,
            reward="Съесть фрукт",
        )

        # Авторизуем первого пользователя по умолчанию
        self.client.force_authenticate(user=self.user1)

    def test_get_habit_list(self):
        """Проверка получения списка привычек владельца."""
        url = reverse("habits:habits-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Ожидаем 2 привычки (приятную и полезную), созданные в setUp
        self.assertEqual(len(response.data["results"]), 2)

    def test_create_habit_success(self):
        """Успешное создание привычки со связанной приятной привычкой."""
        url = reverse("habits:habits-list")
        data = {
            "place": "Офис",
            "time": "12:00:00",
            "action": "Сделать разминку",
            "duration": 90,
            "periodicity": 2,
            "related_habit": self.pleasant_habit.id,
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 3)

    def test_validator_reward_and_related_habit(self):
        """Ошибка: Нельзя одновременно указывать награду и связанную привычку."""
        url = reverse("habits:habits-list")
        data = {
            "place": "Офис",
            "time": "12:00:00",
            "action": "Разминка",
            "reward": "Шоколадка",
            "related_habit": self.pleasant_habit.id,
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Нельзя одновременно заполнять поле вознаграждения", str(response.data))

    def test_validator_duration_limit(self):
        """Ошибка: Время выполнения привычки больше 120 секунд."""
        url = reverse("habits:habits-list")
        data = {
            "place": "Офис",
            "time": "12:00:00",
            "action": "Разминка",
            "duration": 150,  # Больше 120
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("не должно превышать 120 секунд", str(response.data))

    def test_validator_related_habit_must_be_pleasant(self):
        """Ошибка: В связанные привычки нельзя добавить НЕприятную привычку."""
        # Создаем еще одну полезную привычку (is_pleasant=False)
        not_pleasant_habit = Habit.objects.create(
            user=self.user1, place="Дом", time="09:00:00", action="Чтение книги"
        )

        url = reverse("habits:habits-list")
        data = {
            "place": "Офис",
            "time": "12:00:00",
            "action": "Разминка",
            "related_habit": not_pleasant_habit.id,
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("можно выбрать только ту привычку, у которой установлен признак приятной", str(response.data))

    def test_validator_pleasant_habit_restrictions(self):
        """Ошибка: У приятной привычки не может быть вознаграждения."""
        url = reverse("habits:habits-list")
        data = {
            "place": "Дом",
            "time": "21:00:00",
            "action": "Слушать музыку",
            "is_pleasant": True,
            "reward": "Кофе",  # Запрещено для приятной привычки
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("У приятной привычки не может быть вознаграждения", str(response.data))

    def test_validator_periodicity_limit(self):
        """Ошибка: Периодичность выполнения реже, чем раз в 7 дней."""
        url = reverse("habits:habits-list")
        data = {
            "place": "Зал",
            "time": "18:00:00",
            "action": "Тяжелая атлетика",
            "periodicity": 10,  # Реже, чем раз в неделю (максимум 7)
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Нельзя выполнять привычку реже, чем 1 раз в 7 дней", str(response.data))

    def test_habit_access_permission(self):
        """Проверка безопасности: чужой пользователь не может получить доступ к приватной привычке."""
        # Переключаемся на user2
        self.client.force_authenticate(user=self.user2)

        # Пытаемся получить детальную информацию о привычке user1
        url = reverse("habits:habits-detail", args=[self.habit.id])
        response = self.client.get(url)

        # Должен вернуться 404 (так как get_queryset отфильтровал запись и IsOwner заблокировал доступ)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_public_habit_list_api(self):
        """Проверка доступности списка публичных привычек для всех."""
        # Сделаем привычку публичной
        self.habit.is_public = True
        self.habit.save()

        # Разлогиниваемся, имитируя анонимного пользователя
        self.client.logout()

        url = reverse("habits:public_habits")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
