from fastapi import FastAPI, Response, HTTPException
from fastapi import APIRouter, Depends, HTTPException
from app.services.image_processor import ImageProcessor

router = APIRouter()


image_processor = ImageProcessor()


@router.get("/generate-image")
async def generate_image(title: str, subtitle: str):
    try:
        image_bytes = image_processor.add_text_to_image(title, subtitle)
        return Response(content=image_bytes.getvalue(), media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
