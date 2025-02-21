from fastapi import FastAPI

from services.date_time_service import DateTimeFormatter, TimeFormat


app = FastAPI()

formatter = DateTimeFormatter(format=TimeFormat.HUMAN)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/ping")
async def ping():
    return {"message": "pong"}


@app.get("/ping/{ping_id}")
async def ping(ping_id: int):
    return {"message": f"pong {ping_id}"}


@app.get("/time")
async def get_time():
    """Эндпоинт для получения текущего времени"""
    current_time = formatter.get_current_time()
    response = {"current_time": current_time, "time_format": f"{formatter.format}"}
    return response
