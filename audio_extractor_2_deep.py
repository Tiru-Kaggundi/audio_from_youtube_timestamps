import subprocess
import os
import re
from pytube import YouTube


def time_to_seconds(timestamp):
    parts = list(map(int, timestamp.split(':')))
    if len(parts) == 1:
        return parts[0]
    return parts[0] * 60 + parts[1]


def validate_timestamp(timestamp):
    return re.match(r'^\d+:\d{2}$', timestamp)


# Get user input
url = input("Enter YouTube URL: ")
start_time = input("Start time (mm:ss): ")
end_time = input("End time (mm:ss): ")

# Validate timestamps
if not validate_timestamp(start_time) or not validate_timestamp(end_time):
    print("Invalid timestamp format. Use mm:ss.")
    exit()

start = time_to_seconds(start_time)
end = time_to_seconds(end_time)

if start >= end:
    print("End time must be after start time.")
    exit()

try:
    # Download audio
    yt = YouTube(url)
    audio_stream = yt.streams.filter(
        only_audio=True).order_by('abr').desc().first()
    if not audio_stream:
        print("No audio stream found")
        exit()

    temp_file = audio_stream.download(filename_prefix="temp_")

    # Create output filename
    output_file = f"trimmed_audio_{start_time.replace(':', '-')}_{end_time.replace(':', '-')}.mp3"

    # FFmpeg command to trim audio
    command = [
        'ffmpeg',
        '-y',  # Overwrite output file if it exists
        '-i',
        temp_file,
        '-ss',
        str(start),
        '-to',
        str(end),
        '-vn',  # Disable video
        '-acodec',
        'libmp3lame',
        '-q:a',
        '2',  # Audio quality (0-9, 0=best)
        output_file
    ]

    subprocess.run(command, check=True)
    print(f"Successfully created: {output_file}")

except Exception as e:
    print(f"An error occurred: {str(e)}")
finally:
    # Clean up temporary file
    if os.path.exists(temp_file):
        os.remove(temp_file)