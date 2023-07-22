from pytube import YouTube, Playlist
import os
import sys
from tqdm import tqdm
from tkinter import filedialog
from tkinter import Tk
import re


def progress_function(stream, chunk, bytes_remaining):
    current = ((stream.filesize - bytes_remaining) / stream.filesize)
    percent = ('{0:.1f}').format(current * 100)
    progress = int(50 * current)
    sys.stdout.write('\r')
    sys.stdout.write("[%-50s] %s%%" % ('=' * progress, percent))
    sys.stdout.flush()


def get_video_details(url):
    try:
        video = YouTube(url, on_progress_callback=progress_function)
    except Exception as e:
        print(f"Error: {str(e)}")
        return None, None

    streams = video.streams.filter(progressive=True)

    if len(streams) == 0:
        print("No available streams.")
        return None, None

    print(f"\nTitle: {video.title}")
    print("\nAvailable streams:")
    for i, stream in enumerate(streams):
        print(
            f"{i + 1}. {stream.resolution}, {stream.fps}fps, {stream.mime_type}, Size: {round(stream.filesize / (1024 * 1024), 2)}MB")

    return video, streams


def download_video(video, streams, stream_number, download_path):
    if not os.path.exists(download_path):
        print("Invalid download path.")
        return

    if stream_number < 1 or stream_number > len(streams):
        print("Invalid stream number.")
        return

    stream = streams[stream_number - 1]
    print(f"\nDownloading: {stream.resolution}, {stream.fps}fps, {stream.mime_type}")

    try:
        stream.download(download_path)
        print("\nDownload complete!")
    except Exception as e:
        print(f"Error: {str(e)}")


def ask_for_directory():
    root = Tk()
    root.withdraw()
    root.call('wm', 'attributes', '.', '-topmost', True)
    return filedialog.askdirectory()


def is_youtube_playlist(url):
    # Check if the URL is a YouTube playlist link
    return 'youtube.com/playlist' in url


def is_valid_youtube_url(url):
    # YouTube video and playlist URL pattern
    youtube_video_regex = r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|playlist\?list=)[^&=%\?]{11}'
    return re.match(youtube_video_regex, url) is not None


def download_playlist(url, download_path):
    playlist = Playlist(url)

    playlist_folder = os.path.join(download_path, re.sub(r'[^\w\s]', '', playlist.title))
    os.makedirs(playlist_folder, exist_ok=True)

    print(f'Downloading playlist: {playlist.title}')

    playlist_video_urls = playlist.video_urls
    total_videos = len(playlist_video_urls)

    i = 0
    while i < total_videos:
        url = playlist_video_urls[i]
        video, streams = get_video_details(url)
        if video is None or streams is None:
            i += 1
            continue

        stream_number = input(f"Enter the number of the stream you want to download for video {i + 1}/{total_videos} "
                              "(or type 'back' to enter a new URL, 'quit' to exit, 'next' for next video, 'previous' for previous video): ")

        if stream_number.lower() == 'quit':
            return False
        elif stream_number.lower() == 'back':
            return True
        elif stream_number.lower() == 'next':
            if i == total_videos - 1:
                print("This is the last video. No next video available.")
                continue
            else:
                i += 1
                continue
        elif stream_number.lower() == 'previous':
            if i == 0:
                print("This is the first video. No previous video available.")
                continue
            else:
                i -= 1
                continue

        if not stream_number.isdigit() or int(stream_number) < 1:
            print("Invalid stream number.")
            continue
        stream_number = int(stream_number)

        download_video(video, streams, stream_number, playlist_folder)

        i += 1

    return True


def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    while True:
        url = input("Enter the URL of the video or playlist you want to download (or type 'quit' to exit): ")

        if url.lower() == 'quit':
            break

        if not is_valid_youtube_url(url):
            print("Invalid YouTube URL. Please enter a valid YouTube video or playlist URL.")
            continue

        if is_youtube_playlist(url):
            download_path = ask_for_directory()
            if not download_path:
                print("No directory selected.")
                continue

            if not download_playlist(url, download_path):
                continue
        else:
            video, streams = get_video_details(url)

            if video is None or streams is None:
                print("Failed to fetch video details. Please ensure the video URL is correct and try again.")
                continue

            stream_number = input(
                "Enter the number of the stream you want to download (or type 'back' to enter a new URL, 'quit' to exit): ")

            if stream_number.lower() == 'quit':
                break
            elif stream_number.lower() == 'back':
                continue

            if not stream_number.isdigit() or int(stream_number) < 1:
                print("Invalid stream number. Please enter a number corresponding to a video quality option.")
                continue
            stream_number = int(stream_number)

            download_path = ask_for_directory()
            if not download_path:
                print("No directory selected.")
                continue

            download_video(video, streams, stream_number, download_path)


if __name__ == "__main__":
    main()
