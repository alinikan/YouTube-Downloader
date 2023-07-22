from pytube import YouTube, Playlist
import os
import sys
from tkinter import filedialog
from tkinter import Tk
import re


# This function is called periodically to update the progress bar as the video downloads
def progress_function(stream, chunk, bytes_remaining):
    # 'chunk' represents a segment of the media file that has just been downloaded.
    # In this function, it is not currently used, but is included in the function signature
    # because pytube's on_progress_callback expects a function that takes three parameters.
    # It could be used, for example, to calculate download speed.

    # Calculate the current progress as the proportion of the total file size that remains to be downloaded
    current = ((stream.filesize - bytes_remaining) / stream.filesize)
    filled_len = int(round(50 * current))

    # Create a string representing the progress bar. This consists of 'filled' blocks and 'unfilled' dashes.
    bar = '█' * filled_len + '-' * (50 - filled_len)

    # Print the progress bar, overwriting the previous line (hence '\r')
    sys.stdout.write('\r |%s| %s%% ' % (bar, round(current * 100, 1)))

    # Flush the output buffer to ensure that the progress bar is displayed immediately
    sys.stdout.flush()


# This function fetches the details of a YouTube video
def get_video_details(url):
    try:
        # Create a YouTube object, with our progress function as the on_progress_callback
        video = YouTube(url, on_progress_callback=progress_function)
    except Exception as e:
        # If there's an error, print it and return None
        print(f"Error: {str(e)}")
        return None, None

    # Get the available streams of the video
    streams = video.streams.filter(progressive=True)

    # If there are no streams, print a message and return None
    if len(streams) == 0:
        print("No available streams.")
        return None, None

    # Print the video title and the available streams
    print(f"\nTitle: {video.title}")
    print("\nAvailable streams:")
    for i, stream in enumerate(streams):
        print(
            f"{i + 1}. {stream.resolution}, {stream.fps}fps, {stream.mime_type}, Size: {round(stream.filesize / (1024 * 1024), 2)}MB")

    # Return the video and the streams
    return video, streams


# This function downloads a stream of a video
def download_video(video, streams, stream_number, download_path):
    # If the download path doesn't exist, print a message and return
    if not os.path.exists(download_path):
        print("Invalid download path.")
        return

    # If the stream number isn't in the valid range, print a message and return
    if stream_number < 1 or stream_number > len(streams):
        print("Invalid stream number.")
        return

    # Get the selected stream
    stream = streams[stream_number - 1]
    print(f"\nDownloading: {stream.resolution}, {stream.fps}fps, {stream.mime_type}")

    # Try to download the video
    try:
        stream.download(download_path)
        print("\nDownload complete!")
    # If there's an error, print it
    except Exception as e:
        print(f"Error: {str(e)}")


# This function opens a file dialog to ask the user to select a directory
def ask_for_directory():
    # Create a Tk root
    root = Tk()
    # Hide the Tk root
    root.withdraw()
    # Make it topmost
    root.call('wm', 'attributes', '.', '-topmost', True)
    # Open a file dialog and return the selected directory
    return filedialog.askdirectory()


# This function checks if a URL is a YouTube playlist link
def is_youtube_playlist(url):
    return 'youtube.com/playlist' in url


# This function checks if a URL is a valid YouTube video or playlist link
def is_valid_youtube_url(url):
    youtube_video_regex = r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|playlist\?list=)[^&=%\?]{11}'
    return re.match(youtube_video_regex, url) is not None


# This function downloads a YouTube playlist
def download_playlist(url, download_path):
    # Create a Playlist object
    playlist = Playlist(url)

    # Create a folder for the playlist
    playlist_folder = os.path.join(download_path, re.sub(r'[^\w\s]', '', playlist.title))
    os.makedirs(playlist_folder, exist_ok=True)

    print(f'Downloading playlist: {playlist.title}')

    # Get the URLs of the videos in the playlist
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


# This is the main function, which is run when the script starts
def main():
    # Clear the console
    os.system('cls' if os.name == 'nt' else 'clear')

    # Start an infinite loop, which can be exited by typing 'quit'
    while True:
        # Ask the user to input a URL
        url = input("Enter the URL of the video or playlist you want to download (or type 'quit' to exit): ")

        if url.lower() == 'quit':
            break

        # Check if the URL is valid
        if not is_valid_youtube_url(url):
            print("Invalid YouTube URL. Please enter a valid YouTube video or playlist URL.")
            continue

        # Check if the URL is a playlist
        if is_youtube_playlist(url):
            # Ask the user to select a download directory
            download_path = ask_for_directory()
            if not download_path:
                print("No directory selected.")
                continue

            # Download the playlist
            if not download_playlist(url, download_path):
                continue
        else:
            # Get the details of the video
            video, streams = get_video_details(url)

            if video is None or streams is None:
                print("Failed to fetch video details. Please ensure the video URL is correct and try again.")
                continue

            # Ask the user to select a stream to download
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

            # Ask the user to select a download directory
            download_path = ask_for_directory()
            if not download_path:
                print("No directory selected.")
                continue

            # Download the video
            download_video(video, streams, stream_number, download_path)


# This line ensures the main function is run when the script is executed
if __name__ == "__main__":
    main()
