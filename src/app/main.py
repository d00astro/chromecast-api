#!/usr/bin/env python3.8
import logging

from fastapi import FastAPI, Query

from uvicorn import run
from app.routes import cast, status
from app.config import get_settings

from typing import Optional
from starlette.responses import StreamingResponse
from gtts import gTTS, lang
from urllib.parse import urlparse
from io import BytesIO


log = logging.getLogger("uvicorn")

config = get_settings()


def create_api() -> FastAPI:
    fast_api = FastAPI(
        title="Cast API",
        description="""By [Anders Astrom](https://github.com/d00astro)
A simple API for playing audio and voice messages over Chromecast / Home / Nest devices 
""",
        version=config.version,
        openapi_tags=[
            {"name": "status", "description": "Status functions"},
            {"name": "cast", "description": "cast devices"}
        ],
        # root_path=config.route_prefix,
    )
    fast_api.include_router(cast.router, prefix="/cast", tags=["cast"])
    fast_api.include_router(status.router, prefix="/status", tags=["status"])
    return fast_api


api = create_api()


@api.get('/tts/', summary="Text to speech", tags=["util"])
def tts(text: str,
        lang: Optional[str] = Query("en"),
        slow: Optional[bool] = Query(False),
        ):
    """Generate speech audio as an MP3 file from a text.
    - text: Text to synthesise
    - lang: Pronunciation language, as per the '/tts/langs' endpoint
    - slow: Slowed down speech
    """
    log.info(f"Generating speech fot '{text}'")
    if not text:
        return False
    if not lang:
        lang = "en"
    slow = False if not slow else bool(slow)
    speech = gTTS(text=text, lang=lang, slow=slow)
    fp = BytesIO()
    speech.write_to_fp(fp)
    fp.seek(0)
    # w = FileWrapper(fp)
    return StreamingResponse(fp, media_type='audio/mp3')


@api.get('/tts/langs', summary="Supported languages", tags=["util"])
def get_languages():
    """ List supported languages
    """
    return lang.tts_langs()


@api.on_event("startup")
async def startup_event():
    """
    API initialization
    """
    log.info("Starting up...")
    log.info("Pre-loading available Cast-devices")
    cast.get_cast_devices()


@api.on_event("shutdown")
async def shutdown_event():
    """
    API Shutdown procedure
    """
    log.info("Shutting down...")


# For simplified debug purposes only
if __name__ == "__main__":
    run(api, host="0.0.0.0", port=8000)
