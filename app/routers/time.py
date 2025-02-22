from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from app.repositories.time_storage import TimeRepository
from app.dependencies import get_sqlalchemy_repo

router = APIRouter()


# Зависимость для получения репозитория
def get_repository(repo: TimeRepository = Depends(get_sqlalchemy_repo)):
    return repo


@router.post("/write")
async def write_time(repo: TimeRepository = Depends(get_repository)):
    try:
        result = repo.write_time(datetime.utcnow())
        return {"status": "success", "id": result["id"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/read")
async def read_all_records(repo: TimeRepository = Depends(get_repository)):
    records = repo.read_all()
    return {"count": len(records), "data": records}
