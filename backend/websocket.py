from fastapi import WebSocket, WebSocketDisconnect

connections = {
    "ServiciiRelatiiClienti": set(),
    "CallCenter": set(),
    "NOC": set(),
    "Interventii": set(),
}

async def connect(role: str, websocket: WebSocket):
    await websocket.accept()
    connections[role].add(websocket)

async def disconnect(role: str, websocket: WebSocket):
    connections[role].discard(websocket)

async def broadcast(role: str, message: str):
    dead_connections = []
    for ws in connections[role]:
        try:
            await ws.send_text(message)
        except WebSocketDisconnect:
            dead_connections.append(ws)
    for ws in dead_connections:
        connections[role].discard(ws)
