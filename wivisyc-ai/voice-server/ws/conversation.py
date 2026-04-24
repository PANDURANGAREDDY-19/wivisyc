from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()

@router.websocket("/ws/conversation")
async def conversation(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Receive audio chunk from client (binary)
            data: bytes = await websocket.receive_bytes()

            # pipe voice data from STT → LLM → TTS when ready

            # return audio back as the "response" stream
            
            await websocket.send_bytes(data)

    except WebSocketDisconnect:
        pass
