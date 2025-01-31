# IMEI Checker Bot

Этот бот позволяет проверять информацию об устройствах по IMEI через внешний API.


## Установка и запуск

1. Клонируйте репозиторий:
   ```sh
   git clone https://github.com/your-repo/imei-bot.git
   cd imei-bot
   ```

2. Установите зависимости:
   ```sh
   pip install -r requirements.txt
   ```

3. Создайте `.env` файл и добавьте необходимые переменные окружения:
   ```env
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token
   API_AUTH_TOKEN=your_api_auth_token
   API_URL=http://localhost:8000/api/check-imei
   ```

4. Запустите бота:
   ```sh
   python bot.py
   ```

## Использование

1. Запустите бота в Telegram.
2. Отправьте команду `/start`.
3. Введите IMEI (14 или 15 цифр) для проверки.
4. Бот отправит информацию о статусе устройства.

## API

Бот отправляет запрос на API по адресу `http://localhost:8000/api/check-imei`.

**Формат запроса:**
```json
{
    "imei": "123456789012345",
    "token": "your_api_auth_token"
}
```

**Формат ответа:**
```json
{
    "properties": {
        "deviceName": "iPhone 13",
        "gsmaBlacklisted": false,
        "purchaseCountry": "USA",
        "image": "https://example.com/iphone13.jpg"
    }
}
```

## Разрешенные пользователи

Список пользователей, которым доступен бот, задается в `config.py`:
```python
AUTHORIZED_USERS = {123456789, 987654321}
```
Только эти пользователи смогут использовать бота.

## Логирование

Бот записывает ошибки и предупреждения в лог-файл или стандартный вывод. Настройки логирования можно изменить в `bot.py`:
```python
logging.basicConfig(level=logging.INFO)
```

## Развертывание с Docker

1. Соберите Docker-образ:
   ```sh
   docker build -t imei-bot .
   ```
2. Запустите контейнер:
   ```sh
   docker run -d --env-file .env imei-bot
   ```

## Лицензия

Проект распространяется под лицензией MIT.

