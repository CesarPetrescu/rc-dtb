from fastapi import FastAPI, Depends, WebSocket, HTTPException, status, WebSocketDisconnect
from sqlalchemy.orm import Session

from database import Base, engine
from database import SessionLocal
from models import User
from auth import (create_access_token, verify_password, get_password_hash,
                  get_db, ROLES, require_role)
import websocket as ws_manager

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post('/auth/login')
async def login(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

@app.post('/users')
async def create_user(username: str, password: str, role: str, current=Depends(require_role(["ServiciiRelatiiClienti", "CallCenter", "NOC"])), db: Session = Depends(get_db)):
    if role not in ROLES:
        raise HTTPException(status_code=400, detail="Invalid role")
    existing = db.query(User).filter(User.username == username).first()
    if existing:
        raise HTTPException(status_code=400, detail="User exists")
    user = User(username=username, password_hash=get_password_hash(password), role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"id": user.id, "username": user.username, "role": user.role}

@app.websocket('/ws/notifications/{role}')
async def websocket_endpoint(websocket: WebSocket, role: str):
    if role not in ROLES:
        await websocket.close()
        return
    await ws_manager.connect(role, websocket)
    try:
        while True:
            await websocket.receive_text()  # keep alive
    except WebSocketDisconnect:
        await ws_manager.disconnect(role, websocket)
