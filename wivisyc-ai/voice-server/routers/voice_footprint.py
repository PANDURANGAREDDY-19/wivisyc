from fastapi import APIRouter, Request

router = APIRouter()

_store: list[bytes] = []

@router.post("/voice-footprint")
async def voice_footprint(request: Request):
    data = await request.body()
    _store.append(data)
    return {"size": len(data), "status": "received", "index": len(_store) - 1}
