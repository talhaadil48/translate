from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from gtts import gTTS
import uuid
import os
import threading

app = FastAPI()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://sus-forest.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class TTSRequest(BaseModel):
    text: str
    lang: str = "en"

def remove_file_later(file_path: str, delay: int = 15):
    threading.Timer(delay, lambda: os.remove(file_path) if os.path.exists(file_path) else None).start()

@app.post("/translate")
def translate(request: TTSRequest):
    filename = f"{uuid.uuid4().hex}.mp3"
    tts = gTTS(text=request.text, lang=request.lang)
    tts.save(filename)
    remove_file_later(filename)
    return FileResponse(filename, media_type="audio/mpeg", filename=filename)
