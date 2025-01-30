from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from imei_service import IMEIService, IMEIInfo
from utils.imei_validator import validate_imei
import os

app = FastAPI()

API_KEY_HEADER = APIKeyHeader(name="token")

imei_service = IMEIService(api_key=os.getenv("IMEI_CHECK_API_KEY"))

class IMEICheckRequest(BaseModel):
    imei: str

@app.post("/api/check-imei")
async def check_imei(request: IMEICheckRequest, token: str = Depends(API_KEY_HEADER)):
    if token != os.getenv("API_TOKEN"):
        raise HTTPException(status_code=403, detail="Неверный токен авторизации")

    if not validate_imei(request.imei):
        raise HTTPException(status_code=400, detail="Некорректный IMEI")

    try:
        imei_info = imei_service.check_imei(request.imei)
        return imei_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))