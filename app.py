from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import shutil
import whisper
import subprocess

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

model = whisper.load_model("base")

@app.get("/", response_class=HTMLResponse)
def index(request: dict):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload/")
async def upload_video(file: UploadFile, font_size: int = Form(24), font_color: str = Form("FFFFFF")):
    upload_path = Path("uploads") / file.filename
    upload_path.parent.mkdir(exist_ok=True)
    
    with open(upload_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    
    # Transcription
    result = model.transcribe(str(upload_path))
    srt_file = upload_path.with_suffix(".srt")
    
    with open(srt_file, "w", encoding="utf-8") as f:
        for i, segment in enumerate(result["segments"]):
            start = segment["start"]
            end = segment["end"]
            text = segment["text"].strip()
            f.write(f"{i+1}\n")
            f.write(f"{format_time(start)} --> {format_time(end)}\n")
            f.write(f"{text}\n\n")
    
    # Burn subtitles
    output_video = upload_path.with_name(upload_path.stem + "_subtitled.mp4")
    cmd = [
        "ffmpeg", "-i", str(upload_path), "-vf",
        f"subtitles='{srt_file}':force_style='Fontsize={font_size},PrimaryColour=&H{font_color}&'",
        str(output_video)
    ]
    subprocess.run(cmd)
    
    return FileResponse(str(output_video), media_type="video/mp4", filename=output_video.name)

def format_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"
