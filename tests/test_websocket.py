import pytest
from websockets import connect

#
#
# @pytest.mark.asyncio
# async def test_websocket():
#     async with connect("ws://localhost:8000/ws") as websocket:
#         # Подключение успешно
#         await websocket.send("ping")
#         response = await websocket.recv()
#         assert response == "pong"
