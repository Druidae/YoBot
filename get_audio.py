#   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#   THIS IS OLD FILE, PLEASE USING get_audio_async.py
#   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from typing import Any, Literal
import yt_dlp
import os


# Function to get audiofile size from video link
def check_size(url) -> Literal['ok_size', 'too_big_size']:
    # Options for extracting information
    options: dict[str, bool] = {
        "simulate": True
    }

    # Create a YoutubeDL object
    ydl = yt_dlp.YoutubeDL(options)

    # Extract video information
    video_info: dict[str, Any] | None = ydl.extract_info(url=url)

    # Extract formats and find audio formats
    formats = video_info.get("formats", None)
    audio_formats = []

    # Check for audio formats and their file sizes
    for audio_format in formats:
        if audio_format["ext"] == "m4a" or audio_format["ext"] == "webm":
            audio_formats.append(audio_format["filesize"])

    # If the maximum audio file size is less than 20MB, return 'ok_size'
    if max(audio_formats) < 20971520:
        return "ok_size"

    # Otherwise, return 'too_big_size'
    return "too_big_size"


# Function to get audio from video
def get_audio(url) -> str:
    # Extract audio title without downloading
    with yt_dlp.YoutubeDL() as ydl:
        audio_title: str = ydl.sanitize_info(ydl.extract_info(url, download=False))["title"]

    # Define the path where the audio file will be saved
    audio_path = f"data/{audio_title}.mp3"

    # Options for downloading audio
    ydl_opts: dict[str, Any] = {
        "format": "m4a/bestaudio/best",
        "outtmpl": f"data/{audio_title}",  # Output template for downloaded audio file
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",  # Extract audio using FFmpeg
                "preferredcodec": "mp3",  # Preferred audio codec
            }
        ],
    }

    # Download audio using ydl_opts options
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(url)

    # Check the size of the downloaded audio file
    if os.path.getsize(f"data/{audio_title}.mp3") <= 20971520:  # Assuming 20 MB limit
        return audio_path  # Return the path to the audio file

    return "This file is too big"  # Indicate that the file is too big

    # Bellow is the old code it safe for now if we need to back up
    # Remove the downloaded audio file
    # os.remove(f'data/{audio_title}.mp3')

    # return audio
