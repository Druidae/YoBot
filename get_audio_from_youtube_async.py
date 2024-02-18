import yt_dlp
import aiofiles
import os


async def get_info(url):
    options = {
        'simulate': True,
        # 'quiet': True
    }

    ydl = yt_dlp.YoutubeDL(options)

    video_info = ydl.extract_info(url=url)

    formats = video_info.get("formats", None)
    a_formats = []

    for audio_format in formats:
        if audio_format['ext'] == 'm4a' or audio_format['ext'] == 'webm':
            a_formats.append(audio_format['filesize'])

    if max(a_formats) < 20971520:
        return 'ok_size'

    return 'too_big_size'


async def get_audio(url):
    with yt_dlp.YoutubeDL() as ydl:
        info_dict = ydl.extract_info(url, download=False)
        audio_title = ydl.prepare_filename(info_dict)

    audio_path = f'data/{audio_title}.mp3'

    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'outtmpl': f'data/{audio_title}',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    if os.path.getsize(f'data/{audio_title}.mp3') <= 20971520:  # Assuming 20 MB limit
        return audio_path
    else:
        return 'This file is too big'
