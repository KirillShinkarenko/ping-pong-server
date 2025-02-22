from fastapi import FastAPI
from app.database import engine
from app.models.time_record import TimeRecord
from app.routers import time
from app.routers import ping_pong

# Создаем таблицы
TimeRecord.metadata.create_all(bind=engine)


app = FastAPI()
app.include_router(time.router)
app.include_router(ping_pong.router)


@app.get("/")
async def root():
    return {"message": "Time Tracking API"}
