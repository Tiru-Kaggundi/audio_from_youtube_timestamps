import os
from pytube import YouTube
from moviepy.editor import AudioFileClip
import ssl
import certifi
ssl._create_default_https_context = lambda: ssl.create_default_context(cafile=certifi.where())


def mmss_to_seconds(ts):
    try:
        minutes, seconds = ts.strip().split(':')
        return int(minutes) * 60 + int(seconds)
    except Exception:
        raise ValueError("Timestamp must be in mm:ss format")


def main():
    youtube_url = input("Enter the YouTube video URL: ").strip()
    start_ts = input("Enter the start timestamp (mm:ss): ").strip()
    end_ts = input("Enter the end timestamp (mm:ss): ").strip()

    start_time = mmss_to_seconds(start_ts)
    end_time = mmss_to_seconds(end_ts)

    if start_time >= end_time:
        print("Error: The start time must be less than the end time.")
        return

    print("Downloading the audio stream from YouTube...")
    yt = YouTube(youtube_url)
    stream = yt.streams.filter(only_audio=True).first()
    if stream is None:
        print("No audio stream found for this video.")
        return

    # Download the stream; pytube returns the file path.
    temp_filename = "temp_audio"
    file_path = stream.download(filename=temp_filename)
    print("Download complete.")

    print(f"Extracting audio between {start_ts} and {end_ts}...")
    audio_clip = AudioFileClip(file_path)

    if end_time > audio_clip.duration:
        print(
            f"Error: The specified end time exceeds the audio duration ({audio_clip.duration:.2f} seconds)."
        )
        audio_clip.close()
        os.remove(file_path)
        return

    # Create a subclip of the audio between start_time and end_time.
    subclip = audio_clip.subclip(start_time, end_time)

    output_audio = "extracted_audio.mp3"
    subclip.write_audiofile(output_audio)
    print(f"Audio has been extracted and saved as '{output_audio}'.")

    audio_clip.close()
    subclip.close()
    os.remove(file_path)


if __name__ == "__main__":
    main()
