import openai
from pytube import YouTube, request
from pydub import AudioSegment
from pytube.innertube import _default_clients
import os

_default_clients["ANDROID"]["context"]["client"]["clientVersion"] = "19.08.35"
_default_clients["IOS"]["context"]["client"]["clientVersion"] = "19.08.35"
_default_clients["ANDROID_EMBED"]["context"]["client"]["clientVersion"] = "19.08.35"
_default_clients["IOS_EMBED"]["context"]["client"]["clientVersion"] = "19.08.35"
_default_clients["IOS_MUSIC"]["context"]["client"]["clientVersion"] = "6.41"
_default_clients["ANDROID_MUSIC"] = _default_clients["ANDROID_CREATOR"]

# download the youtube videos
def download_audio(youtube_url, output_filename="audio.mp3"):
    yt = YouTube(youtube_url)
    for stream in yt.streams:
        print(stream)

    # download video
    request.default_range_size = 0
    video = yt.streams.filter(only_audio=True).all()
    downloaded_file = video.download(filename="temp_video")
    
    # convert the downloaded file to mp3 using pydub
    audio = AudioSegment.from_file(downloaded_file)
    audio.export(output_filename, format="mp3")
    os.remove(downloaded_file)  # remove temp video file
    return output_filename

# return transcription of the video
def transcription(path):
    with open(path, "rb") as audio:
        response = openai.Audio.transcribe("whisper-1", audio)
    return response['text']

# download_audio(youtube_url="https://youtu.be/jejgP_u82Qo?si=aKWIgg_d1JB2ocIT")
print(transcription("practice.mp3"))