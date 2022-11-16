import asyncio
import json
from typing import Union

import websockets
from websockets.legacy.server import WebSocketServerProtocol
from websockets.exceptions import ConnectionClosed


from collections_coord import InMemoryCollection
from collections_coord import ReaderCollection


class SocketServer:
    HOST: str = "localhost"
    PORT: int = 25000
    FREQUENCY: float = 1.0

    def __init__(self,
                 coord_collection: Union[InMemoryCollection,
                                         ReaderCollection],
                 host: str = HOST,
                 port: int = PORT) -> None:
        self.coord_collection: Union[InMemoryCollection,
                                     ReaderCollection] = coord_collection
        self._host: str = host
        self._port: int = port

    async def _conn_handler(self, websocket: WebSocketServerProtocol) -> None:
        async for row in self.coord_collection.get_iterator():
            data: str = json.dumps(row)
            try:
                await websocket.send(data)
            except ConnectionClosed:
                break
            await asyncio.sleep(self.FREQUENCY)

    async def serve_socket(self) -> None:
        if self.coord_collection.is_data is False:
            await self.coord_collection.collect()
        async with websockets.serve(self._conn_handler, self._host, self._port):
            await asyncio.Future()  # run forever

    def start(self) -> None:
        asyncio.run(self.serve_socket())


if __name__ == '__main__':

    import os
    resource_path: str = os.path.join(
        "/mnt/f/codeCoolHomework/homeworkNorbit_másolata/socket_boat_position", "lines")
    collection = InMemoryCollection(resource_path)
    server = SocketServer(collection)
    server.start()
