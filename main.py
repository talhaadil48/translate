from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from gtts import gTTS
from io import BytesIO

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for quick testing; use specific domains in prod
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/")
async def translate(request: Request):
    body = await request.json()
    text = body.get("text", "")
    lang = body.get("lang", "en")

    if not text:
        return {"error": "Text is required"}

    mp3_fp = BytesIO()
    tts = gTTS(text=text, lang=lang)
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)

    return StreamingResponse(mp3_fp, media_type="audio/mpeg")
