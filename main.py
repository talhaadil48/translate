from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from gtts import gTTS
import uuid
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://sus-forest.vercel.app"
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

TMP_DIR = "/tmp"  # Vercel allows /tmp for temp file writes

@app.post("/translate")
async def translate(request: Request):
    body = await request.json()
    text = body.get("text", "")
    lang = body.get("lang", "en")

    if not text:
        return JSONResponse(status_code=400, content={"error": "Text is required"})

    try:
        filename = f"{uuid.uuid4().hex}.mp3"
        filepath = os.path.join(TMP_DIR, filename)

        tts = gTTS(text=text, lang=lang)
        tts.save(filepath)

        return FileResponse(
            filepath,
            media_type="audio/mpeg",
            filename="output.mp3",
            headers={"Content-Disposition": "inline; filename=output.mp3"}
        )

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
