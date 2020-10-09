import os;
from pydantic import BaseModel
from fastapi import APIRouter, Request, Query, Depends, Path as PathParam
from typing import Optional, List
from starlette.responses import FileResponse, StreamingResponse
import socket
import pychromecast
import logging
from gtts import gTTS
from slugify import slugify
from pathlib import Path
from urllib.parse import urlparse
from io import BytesIO
from functools import lru_cache

router = APIRouter()
log = logging.getLogger('uvicorn')


class CastInfo(BaseModel):
    name: str
    friendly_name: str
    model_name: str
    cast_type: str
    manufacturer: str
    uri: str
    uuid: str


def connect(device_name):
    """Connect to a Cast device
    - device_name: Name of device to connect to
    """
    log.info(f"Connecting to '{device_name}'")
    connection, _ = pychromecast.get_listed_chromecasts(friendly_names=[device_name])
    cast_device = connection[0]
    cast_device.wait()
    log.info(f"Connected to '{device_name}'")
    return cast_device


def discover_cast_devices():
    """Discover Cast devices on network
    """
    log.info("Discovering Cast services on the network")
    services, browser = pychromecast.discovery.discover_chromecasts()
    pychromecast.discovery.stop_discovery(browser)
    log.info(f"Found {len(services)} services")
    return dict([(slugify(name), connect(name)) for (cast_device, uuid, model, name, ip, port) in services])


@lru_cache
def get_cast_devices():
    """Get a dictionary of all available Cast devices on the network
    """
    log.info("Getting available Cast services")
    _cast_devices = discover_cast_devices()
    for lookup_name, cast in _cast_devices.items():
        log.info(f"{lookup_name}: {cast}")
    log.info("Service listing complete")
    return _cast_devices


# # just for pre-loading
# _devs = get_cast_devices()
#
#
# def get_cast_device(name):
#     return get_cast_devices()[name]


def resolve(netloc):
    """
    Resloves the domain / hostname of a network location/address to IP address.
    This is because for some reason Google's Cast devices only seem to like requesting media from IP-based locations.
    """
    log.info(f"Resolving hostname '{netloc}'")
    netlocs = netloc.split(':')
    netlocs[0] = socket.gethostbyname(netlocs[0])
    netloc = ":".join(netlocs)
    log.info(f"Resolved to: {netloc}")
    return netloc


# TODO: this functionality should be with the normal '/tts' endpoint
def rec_tts_url(request, text, lang=None, slow=None):
    """Get a pre-recorded/cached url for text-to-speech audio.
    This will generate and store the audio locally, if already exists.
    - text: Text to synthesise
    - lang: Pronunciation language, as per the '/tts/langs' endpoint
    - slow: Slowed down speech
    """
    if lang is None:
        lang = "en"
    if slow is None:
        slow = False

    filename = slugify(text+"-"+lang+"-"+str(slow)) + ".mp3"
    rec_dir = "static/recordings"
    cache_filename = f"./{rec_dir}/{filename}"
    tts_file = Path(cache_filename)
    log.info(f"TTS File: {tts_file}")

    if not tts_file.is_file():
        log.info(f"The file '{tts_file}' does not exist.")
        tts = gTTS(text=text, lang=lang, slow=slow)
        tts.save(cache_filename)

    urlparts = request.url
    mp3_url = f"{urlparts.scheme}://{resolve(urlparts.netloc)}/{rec_dir}/{filename}"
    log.info(f'Recorded mp3: {mp3_url}')
    return mp3_url


# TODO: this functionality should be with the normal '/tts' endpoint
def live_tts_url(request, text, lang=None, slow=None):
    """Get an on-demand url for text-to-speech audio.
    This will not generate the audio, until the url is called, and the audio will not be stored.
    - text: Text to synthesise
    - lang: Pronunciation language, as per the '/tts/langs' endpoint
    - slow: Slowed down speech
    """
    urlparts = request.url
    mp3_url = f"{urlparts.scheme}://{resolve(urlparts.netloc)}/tts/?text={text}"
    if lang is not None:
        mp3_url += f"&lang={lang}"
    if slow is not None:
        mp3_url += f"&slow={slow}"
    log.info(f'Live mp3: {mp3_url}')
    return mp3_url


def play_mp3(cast_device, mp3_url):
    """Request a Cast device to play an MP3 from an URL
    """
    cast_device.wait()
    mc = cast_device.media_controller
    mc.stop()
    mc.play_media(mp3_url, 'audio/mp3')
    mc.block_until_active()


@router.get("/devices", summary="List available devices", response_model=List[CastInfo])
def get_devices(devices=Depends(get_cast_devices)):
    """List available Cast devices
    """
    listing = []
    for lookup_name, cast in devices.items():
        info = CastInfo(
            name=lookup_name,
            friendly_name=cast.device.friendly_name,
            model_name=cast.device.model_name,
            manufacturer=cast.device.manufacturer,
            uri=str(cast.uri),
            uuid=str(cast.device.uuid),
            cast_type=cast.device.cast_type
        )
        listing.append(info)

    return listing


# TODO: this functionality should not be with the cast stuff, maybe with the '/tts' endpoint
# Should probably be handled with fastapi.mount and StaticFiles instead
@router.get('/static/{path}', summary="Get static resource")
def send_static(path: str = PathParam(..., title="Path", description="Path to static resource")):
    """Get a local static media resource
    - path : Path to local media
    """
    log.info(f"get static: '{path}'")
    logging.info(f"get static: '{path}'")
    return FileResponse(f'static/{path}')


@router.get('/{device_name}/play/{filename}', summary="Cast audio")
def play(
        request: Request,
        device_name: str = PathParam(..., title="Device Name", description="Name of Cast device or group to play on"),
        filename: str = PathParam(..., title="File to play", description="File to play"),
        devices=Depends(get_cast_devices)
):
    """Request to play media on cast device or group
    - device_name: name of device or device group to cast to
    - filename: name of media to play
    """
    log.info(f"get static: '{filename}'")
    urlparts = request.url
    mp3 = Path(f"./static/{filename}")
    if mp3.is_file():
        mp3_url = f"{urlparts.scheme}://{resolve(urlparts.netloc)}/static/{filename}"
    else:
        mp3_url = filename

    device = devices[device_name]

    play_mp3(device, mp3_url)
    return filename


@router.get('/{device_name}/say/', summary="Cast speech")
def say(request: Request,
        device_name,
        text: str,
        lang: Optional[str] = Query("en"),
        slow: Optional[bool] = Query(False),
        rec: Optional[bool] = Query(False),
        devices=Depends(get_cast_devices)
        ):
    """Request cast device or group to say somethting
    - device_name: Name of device to request
    - text: Text to speak
    - lang: Pronunciation language
    - slow: Speak slower
    - rec: Record speech
    """
    if not text:
        return False
    log.info(f"About to say: '{text}`")
    if not rec:
        speech_url = live_tts_url(request, text, lang=lang, slow=slow)
    else:
        speech_url = rec_tts_url(request, text, lang=lang, slow=slow)
    device = devices[device_name]
    play_mp3(device, speech_url)
    return text



