import openai
from pytube import YouTube, request
from pydub import AudioSegment
from pytube.innertube import _default_clients
import os
import openai_secrets

_default_clients["ANDROID"]["context"]["client"]["clientVersion"] = "19.08.35"
_default_clients["IOS"]["context"]["client"]["clientVersion"] = "19.08.35"
_default_clients["ANDROID_EMBED"]["context"]["client"]["clientVersion"] = "19.08.35"
_default_clients["IOS_EMBED"]["context"]["client"]["clientVersion"] = "19.08.35"
_default_clients["IOS_MUSIC"]["context"]["client"]["clientVersion"] = "6.41"
_default_clients["ANDROID_MUSIC"] = _default_clients["ANDROID_CREATOR"]

transcription_result_file = "transcription_result.txt"

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

# helper function to make timestamps formatting in minutes/seconds
def format_timestamp(seconds):
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"

# transcribe audio with timestamps
def transcription_w_timestamps(path):
    openai.api_key = openai_secrets.SECRET_KEY

    with open(path, "rb") as audio_file:
        response = openai.Audio.transcribe(
            model="whisper-1", 
            file=audio_file, 
            response_format="verbose_json"
        )

    with open(transcription_result_file, "w") as output_file:
        for segment in response['segments']:
            output_file.write((f"[{format_timestamp(segment['start'])} - {format_timestamp(segment['end'])}] {segment['text']} \n"))

# download_audio(youtube_url="https://youtu.be/jejgP_u82Qo?si=aKWIgg_d1JB2ocIT")
transcription_w_timestamps("practice.mp3")