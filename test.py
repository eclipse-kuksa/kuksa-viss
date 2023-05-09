#!/usr/bin/env python

import asyncio
import websockets


async def hello():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri,subprotocols=["VISSv2"]) as websocket:
        #name = input("What's your name? ")

        await websocket.send('''{"action: 34"lol"}''')
        rep=greeting = await websocket.recv()
        print(f"<<< {rep}")

        await websocket.send('''{"action": "lol"}''')
        rep=greeting = await websocket.recv()
        print(f"<<< {rep}")


        await websocket.send('''{"action": "get"}''')
        rep=greeting = await websocket.recv()
        print(f"<<< {rep}")

        await websocket.send('''{"action": "get", "path": "Vehicle.Speeeeed", "requestId":"sddf"}''')
        rep=greeting = await websocket.recv()
        print(f"<<< {rep}")

        await websocket.send('''{"action": "get", "path": "Vehicle.Speed", "requestId":"sddf"}''')
        rep=greeting = await websocket.recv()
        print(f"<<< {rep}")

        await websocket.send('''{"action": "get", "path": "Vehicle.OBD.Speed", "requestId":"sddf"}''')
        rep=greeting = await websocket.recv()
        print(f"<<< {rep}")


        print(f"SEEEEEEEEEET")


        await websocket.send('''{"action": "set"}''')
        rep=greeting = await websocket.recv()
        print(f"<<< {rep}")

        await websocket.send('''{"action": "set", "path": "Vehicle.Speed", "requestId":"sddf"}''')
        rep=greeting = await websocket.recv()
        print(f"<<< {rep}")

        await websocket.send('''{"action": "set", "path": "Vehicle.Speed", "value": "400", "requestId":"sddf"}''')
        rep=greeting = await websocket.recv()
        print(f"<<< {rep}")


        

if __name__ == "__main__":
    asyncio.run(hello())