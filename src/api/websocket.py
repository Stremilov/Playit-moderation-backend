from fastapi import APIRouter, WebSocket, Depends, WebSocketDisconnect, Request
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates

from api.tasks import get_pending_tasks
from core.db import get_db_session
from utils.websocket_connection_Maneger import ConnectionManager

router = APIRouter(tags=["websocket"])
manager = ConnectionManager()


# TODO: сделать Сессию ассинхронной не забудь
@router.websocket("/ws")
async def update_tasks_realtime(
    websocket: WebSocket, session: Session = Depends(get_db_session)
):
    await manager.connect(websocket)
    try:
        while True:
            tasks = await get_pending_tasks(session)
            await manager.broadcast({"Tasks updated": tasks})
    except WebSocketDisconnect:
        manager.disconnect(websocket=websocket)
