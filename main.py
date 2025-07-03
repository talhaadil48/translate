from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from gtts import gTTS
import io

app = FastAPI()

# CORS setup
origins = [
    "https://sus-forest.vercel.app",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TTSRequest(BaseModel):
    text: str
    lang: str = "en"

@app.post("/translate")
async def translate(request: Request):
    data = await request.json()
    text = data.get("text")
    lang = data.get("lang", "en")

    mp3_fp = io.BytesIO()
    tts = gTTS(text=text, lang=lang)
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)

    return StreamingResponse(mp3_fp, media_type="audio/mpeg")


