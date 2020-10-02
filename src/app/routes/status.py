from fastapi import APIRouter, Depends
from app.config import get_settings, Settings

router = APIRouter()


@router.get("/")
async def status(settings: Settings = Depends(get_settings)):
    """
    ### Gets API status
    """
    return {
        "status": "running",
        "environment": settings.environment,
        "testing": settings.testing,
    }
