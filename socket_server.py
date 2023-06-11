import asyncio
import threading

import websockets
from websockets.server import serve


class CozyWebSocketServer:
    def __init__(self, host='127.0.0.1', port=8765):
        self.host = host
        self.port = port
        self.server = None

    async def handle_client(self, websocket, path):
        while True:
            # Handle incoming messages from the client
            data = await websocket.recv()
            await self.process_message(websocket, data)

    async def process_message(self, websocket, data):
        # Process the received message from the client
        print(f"Received message: {data}")

        # Example: Send a response back to the client
        response = f"Server received: {data}"
        await websocket.send(response)

    async def start(self, stopper):
        # self.server = websockets.serve(self.handle_client, self.host, self.port)
        # asyncio.get_event_loop().run_until_complete(self.server)
        # asyncio.get_event_loop().run_forever()
        print(f"Starting socket server on {self.host}:{self.port}...")
        stop = asyncio.Future()
        async with serve(self.handle_client, self.host, self.port, ssl=None):
            while True:
                await asyncio.sleep(1)
                if stopper.is_set():
                    print(f"Stopping socket server...")
                    stop.set_result(True)
                    break

    def stop(self):
        if self.server is not None:
            self.server.close()
            asyncio.get_event_loop().run_until_complete(self.server.wait_closed())


def main(stopper):
    def instantiate():
        server = CozyWebSocketServer()
        asyncio.run(server.start(stopper))

    thread = threading.Thread(target=instantiate)
    thread.start()
    return thread
