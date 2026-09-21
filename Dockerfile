FROM python:3.12-slim

# Системные настройки для вывода логов без задержек
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Устанавливаем только самые необходимые системные библиотеки базы данных
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Шаг-трюк: ставим утилиту poetry через стандартный pip, выгружаем зависимости
# в requirements.txt и сразу же ставим их напрямую в систему контейнера.
# Это убирает любую магию скрытых путей виртуальных окружений!
COPY pyproject.toml poetry.lock* ./
RUN pip install --no-cache-dir poetry \
    && poetry export -f requirements.txt --output requirements.txt --without-hashes \
    && pip install --no-cache-dir -r requirements.txt \
    && pip uninstall -y poetry

# Копируем весь остальной код вашего трекера привычек
COPY . .

EXPOSE 8000