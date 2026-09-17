import requests
from django.conf import settings


def send_telegram_message(chat_id: str, message: str) -> None:
    """Отправляет текстовое сообщение в Telegram-чат через бота."""
    # Получаем токен из переменных окружения (через settings)
    bot_token = getattr(settings, "TELEGRAM_BOT_TOKEN", None)

    if not bot_token:
        print("Ошибка: TELEGRAM_BOT_TOKEN не настроен в конфигурации.")
        return

    url = f"https://telegram.org{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Ошибка при отправке сообщения в Telegram: {e}")
