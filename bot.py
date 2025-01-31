import logging
import httpx
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv
from config import TELEGRAM_BOT_TOKEN, API_AUTH_TOKEN, AUTHORIZED_USERS, API_URL

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=TELEGRAM_BOT_TOKEN, default=DefaultBotProperties(parse_mode="Markdown"))
dp = Dispatcher()

def is_authorized(user_id: int) -> bool:
    """Проверяет, есть ли пользователь в белом списке."""
    return user_id in AUTHORIZED_USERS


def validate_imei(imei: str) -> bool:
    """Проверяет, что IMEI состоит из 14 или 15 цифр."""
    return imei.isdigit() and len(imei) in (14, 15)


async def fetch_imei_info(imei: str) -> dict:
    """
    Отправляет запрос к API для проверки IMEI.
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                API_URL,
                json={"imei": imei, "token": API_AUTH_TOKEN},
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"Ошибка API: {e.response.text}")
            raise Exception("Ошибка на стороне сервера.")
        except httpx.RequestError as e:
            logger.error(f"Ошибка сети: {e}")
            raise Exception("Не удалось подключиться к серверу.")
        except Exception as e:
            logger.error(f"Непредвиденная ошибка: {e}")
            raise Exception("Произошла ошибка при обработке IMEI.")


@dp.message(Command("start"))
async def start(message: Message):
    """Отправляет приветственное сообщение."""
    if not is_authorized(message.from_user.id):
        await message.answer("У вас нет доступа к этому боту.")
        return
    await message.answer("Отправьте IMEI для проверки.")


@dp.message()
async def check_imei(message: Message):
    """Обрабатывает IMEI и отправляет запрос на API."""
    if not is_authorized(message.from_user.id):
        await message.answer("У вас нет доступа к этому боту.")
        return

    imei = message.text.strip()
    if not validate_imei(imei):
        await message.answer("⚠Некорректный IMEI. IMEI состоит из 14 или 15 цифр.")
        return

    await message.answer("🔍 Проверяем IMEI...")

    try:
        data = await fetch_imei_info(imei)

        properties = data.get("properties", {})
        if not properties:
            await message.answer("Данные по этому IMEI не найдены.")
            return

        imei_info = (
            f"- Информация по IMEI {imei}:\n"
            f"- Модель устройства: {properties.get('deviceName', '❓ Нет данных')}\n"
            f"- Заблокирован ли по GSMA: {'Да' if properties.get('gsmaBlacklisted') else 'Нет'}\n"
            f"- Страна покупки**: {properties.get('purchaseCountry', 'Нет данных')}\n"
        )

        image_url = properties.get("image")
        if image_url:
            imei_info += f"Фото устройства: [Изображение]({image_url})\n"

        await message.answer(imei_info)
    except Exception as e:
        await message.answer(str(e))


async def main():
    """Запускает бота."""
    async with bot:
        await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
