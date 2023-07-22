from pytube import YouTube
import os
import sys
from tqdm import tqdm

def progress_function(stream, chunk, bytes_remaining):
    current = ((stream.filesize - bytes_remaining)/stream.filesize)
    percent = ('{0:.1f}').format(current*100)
    progress = int(50*current)
    sys.stdout.write('\r')
    sys.stdout.write("[%-50s] %s%%" % ('='*progress, percent))
    sys.stdout.flush()

def get_video_details(url):
    try:
        # on_progress_callback argument is used to show the download progress
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
        print(f"{i + 1}. {stream.resolution}, {stream.fps}fps, {stream.mime_type}, Size: {round(stream.filesize/(1024*1024),2)}MB")

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


def main():
    url = input("Enter the URL of the video you want to download: ")

    video, streams = get_video_details(url)

    if video is None or streams is None:
        return

    stream_number = input("Enter the number of the stream you want to download: ")

    if not stream_number.isdigit() or int(stream_number) < 1:
        print("Invalid stream number.")
        return
    stream_number = int(stream_number)

    download_path = input("Enter the download path: ")
    download_video(video, streams, stream_number, download_path)


if __name__ == "__main__":
    main()
