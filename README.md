# Subtitles

A web app to automatically add subtitles to uploaded videos using Whisper AI.

## Features
- Upload videos
- Automatic transcription
- Subtitle customization (font size, color)
- Download video with burned-in subtitles

## Setup
1. Clone the repo.
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the app:
   ```
   uvicorn app:app --reload
   ```
4. Open your browser at `http://127.0.0.1:8000/`

## Notes
- Make sure `ffmpeg` is installed on the server.
- Subtitles are burned into the video using ffmpeg.
