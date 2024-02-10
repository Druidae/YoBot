import yt_dlp
import os
import json


def get_info(url):
    with yt_dlp.YoutubeDL() as ydl:
        audio_info = ydl.extract_info(url, download=False)

    audio_info_json = json.dumps(audio_info)

    return audio_info_json


def get_audio(url):
    # urls = [url]
    ydl_opts = {}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        audio_title = ydl.sanitize_info(ydl.extract_info(url, download=False))['title']

    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'outtmpl': f'data/{audio_title}',
        'postprocessors': [{  # Extract audio using ffmpeg
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(url)

    audio = open(f'data/{audio_title}.mp3', 'rb')
    os.remove(f'data/{audio_title}.mp3')

    return audio


# if __name__ == '__main__':
    # print(get_info('https://youtu.be/7HP0cOGbz_Y?si=1oU7pM-tRnsMC7NM'))
#     get_audio(' https://youtu.be/7HP0cOGbz_Y?si=1oU7pM-tRnsMC7NM')
