from src import InMemoryCollection
from src import SocketServer

RESOURCE_PATH: str = ''

collection = InMemoryCollection(RESOURCE_PATH)
server = SocketServer(collection)
server.start()