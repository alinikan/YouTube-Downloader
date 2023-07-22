# Python YouTube Downloader

This Python YouTube Downloader is a script that allows users to download videos or playlists from YouTube. It is developed using the `pytube` library and has a console-based interface. Users can choose the desired resolution and format from the available streams of the videos.

## Features

- Download individual YouTube videos.
- Download entire YouTube playlists.
- Choose video quality and format.
- Monitor download progress in the terminal.

## Requirements

- Python 3.6 or later.
- `pytube` library for Python.
- `tkinter` library for Python.
- `os`, `sys` and `re` modules from Python standard library.

## Installation

1. Install Python 3.6 or later.
2. Clone this repository to your local machine.
3. Navigate to the cloned repository's directory.
4. Install the necessary libraries using pip:

```bash
pip install pytube tkinter
```
or
```bash
pip3 install pytube tkinter
```

## Usage
1. Run the script:

```bash
python main.py
```
or
```bash
python3 main.py
```

2. Enter the URL of the video or playlist you want to download when prompted.
3. If the URL is a video, you will be shown the available streams for that video. Enter the number of the stream you want to download.
4. If the URL is a playlist, you will be prompted to choose a stream for each video. You can navigate between the videos by typing 'next' or 'previous'.
5. When asked, choose a directory to save the downloaded video or playlist.
6. The video will start downloading and the progress will be shown in the terminal.