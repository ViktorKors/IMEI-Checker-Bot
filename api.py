import logging
import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from config import API_SANDBOX_TOKEN, API_AUTH_TOKEN, IMEI_API_URL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


class IMEIRequest(BaseModel):
    imei: str
    token: str


def verify_auth_token(token: str):
    """
    Проверяет авторизационный токен API.
    """
    if token != API_AUTH_TOKEN:
        raise HTTPException(status_code=403, detail="Неверный API-токен")


async def fetch_imei_info(imei: str) -> dict:
    """
    Отправляет запрос к API imeicheck.net и получает информацию по IMEI.
    """
    headers = {"Authorization": f"Bearer {API_SANDBOX_TOKEN}", "Content-Type": "application/json"}
    json_data = {"deviceId": imei, "serviceId": 12}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(IMEI_API_URL, headers=headers, json=json_data)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            logger.error(f"Ошибка API imeicheck.net: {e.response.text}")
            raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
        except httpx.RequestError as e:
            logger.error(f"Ошибка сети: {e}")
            raise HTTPException(status_code=500, detail="Ошибка соединения с API")

    return response.json()


@app.post("/api/check-imei")
async def check_imei(request: IMEIRequest):
    """
    Проверяет IMEI через imeicheck.net API.
    """
    verify_auth_token(request.token)

    if not request.imei.isdigit() or len(request.imei) not in (14, 15):
        raise HTTPException(status_code=400, detail="Некорректный формат IMEI")

    return await fetch_imei_info(request.imei)
