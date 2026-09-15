from datetime import datetime
from celery import shared_task
from habits.models import Habit
from habits.services import send_telegram_message


@shared_task
def send_habit_reminders():
    """Фоновая задача для рассылки напоминаний о привычках по расписанию."""
    # Получаем текущее время (часы и минуты)
    now = datetime.now().time()
    current_hour_minute = now.replace(second=0, microsecond=0)

    # Ищем все привычки, у которых время совпадает с текущим
    # И у создателей которых заполнен telegram_chat_id
    habits = Habit.objects.filter(
        time__hour=current_hour_minute.hour,
        time__minute=current_hour_minute.minute,
        user__telegram_chat_id__isnull=False,
    ).select_related("user")

    for habit in habits:
        # Формируем текст напоминания
        message = (
            f"Напоминание! Время для полезной привычки:\n"
            f"Вы обещали: {habit.action} в {habit.time.strftime('%H:%M')} в {habit.place}.\n"
        )

        if habit.reward:
            message += f"Награда за выполнение: {habit.reward} 🎁"
        elif habit.related_habit:
            message += (
                f"Затем вас ждет приятная привычка: {habit.related_habit.action} 🎉"
            )

        # Отправляем сообщение через наш сервис
        send_telegram_message(
            chat_id=habit.user.telegram_chat_id, message=message
        )
