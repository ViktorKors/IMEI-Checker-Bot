# Используем минимальный образ Python
FROM python:3.12

# Устанавливаем переменные окружения
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    WORKDIR=/app

# Создаём рабочую директорию
WORKDIR $WORKDIR

# Копируем зависимости и устанавливаем их
COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry install --only main --no-root

# Копируем код приложения
COPY . .

# Запускаем FastAPI и бота в отдельных процессах
CMD ["sh", "-c", "poetry run uvicorn api:app --host 0.0.0.0 --port 8000 & poetry run python bot.py"]
