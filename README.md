# YouTube Video Downloader

This project is a simple Python-based YouTube video downloader that allows users to download videos directly from YouTube by providing the video URL. The downloader supports downloading videos in various resolutions and formats, making it a versatile tool for offline viewing.

## Features
- Download videos in different resolutions (144p, 360p, 720p, 1080p, etc.)
- Support for multiple formats (MP4, WebM, etc.)
- Easy-to-use interface for inputting the video URL
- Error handling for invalid URLs or unsupported videos

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/GouthamOfTheNP/YouTubeVidDownloader.git
    ```
2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
1. Run the Python script:
    ```bash
    python main.py
    ```
2. Input the YouTube video URL when prompted, select the desired resolution/format, and download the video.
3. If you want to make this an app, run:
    ```bash
    pyinstaller main.py --windowed --icon=ytvid.png
    ```

## License
This project is licensed under the MIT License, allowing for any use of this code with attribution.
