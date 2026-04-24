from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import voice_footprint, tts_stream
from ws.conversation import router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["Frontend-Port"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(voice_footprint.router)
app.include_router(tts_stream.router)
app.include_router(router)