from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

router = APIRouter()

CHUNK_SIZE = 2048

@router.post("/tts-stream")
async def tts_stream(request: Request):
    data = await request.body()
    content_type = request.headers.get("""audio/""")

    async def stream():
        for i in range(0, len(data), CHUNK_SIZE):
            yield data[i:i + CHUNK_SIZE]

    return StreamingResponse(stream(), media_type=content_type)
