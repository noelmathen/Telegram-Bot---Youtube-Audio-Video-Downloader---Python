# YouTube Downloader Telegram Bot

## Project Description

The YouTube Downloader Telegram Bot is a Python-based bot that enables users to effortlessly download YouTube videos and playlists directly from Telegram. The bot supports both video (mp4) and audio (mp3) formats, providing users with flexibility based on their preferences.

## Key Features

### Single Video Download

- Users can input a valid YouTube video link, and the bot will download the video in 360p resolution as an mp4 file.

### Single Audio Download

- Users have the option to request audio-only versions of YouTube videos, which will be downloaded as mp3 files.

### Playlist Video Download

- The bot can handle YouTube playlist links, downloading all the videos in the playlist as mp4 files in 360p resolution.

### Playlist Audio Download

- Users can also download all the audio tracks from a YouTube playlist, saving them as mp3 files.

## Usage and Limitations

- The bot supports video downloads for YouTube links with resolutions up to 360p.
- Videos or playlists exceeding 8 minutes in length cannot be downloaded due to size limitations (maximum 30MB per file).
- For playlist downloads, the bot will send each video or audio as individual files.
