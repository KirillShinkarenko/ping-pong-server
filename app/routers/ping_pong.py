from fastapi import APIRouter, Depends
from app.models.time_format import TimeFormat
from app.repositories.date_time_service import DateTimeFormatter


formatter = DateTimeFormatter(format=TimeFormat.HUMAN)

router = APIRouter()


@router.get("/ping")
async def ping():
    return {"message": "pong"}


@router.get("/ping/{ping_id}")
async def ping(ping_id: int):
    return {"message": f"pong {ping_id}"}


@router.get("/time")
async def get_time():
    """Эндпоинт для получения текущего времени"""
    current_time = formatter.get_current_time()
    response = {"current_time": current_time, "time_format": f"{formatter.format}"}
    return response
