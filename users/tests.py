from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User


class UserRegistrationTests(APITestCase):
    """Тестирование регистрации пользователей."""

    def test_register_user(self):
        """Проверка успешной регистрации нового пользователя."""
        url = reverse("users:register")
        data = {
            "email": "testuser@example.com",
            "password": "securepassword123",
            "telegram_chat_id": "123456789",
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, "testuser@example.com")
        self.assertNotIn("password", response.data)  # Пароль не должен возвращаться в ответе
