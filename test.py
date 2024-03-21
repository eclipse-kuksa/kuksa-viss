#!/usr/bin/env python

import asyncio
import websockets


async def hello():
    uri = "ws://localhost:8090"
    async with websockets.connect(uri, subprotocols=["VISSv2"]) as websocket:
        # name = input("What's your name? ")

        await websocket.send('''{"action: 34"lol"}''')
        rep = await websocket.recv()
        print(f"<<< {rep}")

        await websocket.send('''{"action": "lol"}''')
        rep = await websocket.recv()
        print(f"<<< {rep}")

        await websocket.send('''{"action": "get"}''')
        rep = await websocket.recv()
        print(f"<<< {rep}")

        await websocket.send('''{"action": "get", "path": "Vehicle.Speeeeed", "requestId":"sddf"}''')
        rep = await websocket.recv()
        print(f"<<< {rep}")

        await websocket.send('''{"action": "get", "path": "Vehicle.Speed", "requestId":"sddf"}''')
        rep = await websocket.recv()
        print(f"<<< {rep}")

        await websocket.send('''{"action": "get", "path": "Vehicle.OBD.Speed", "requestId":"sddf"}''')
        rep = await websocket.recv()
        print(f"<<< {rep}")

        await websocket.send('''{"action": "getMetaData", "path": "Vehicle.OBD.Speed", "requestId":"sddf"}''')
        rep = await websocket.recv()
        print(f"<<< {rep}")

        await websocket.send('''{"action": "getMetaData", "path": "Vehicle.NotExist", "requestId":"sddf"}''')
        rep = await websocket.recv()
        print(f"<<< {rep}")

        await websocket.send('''{"action": "provide", "path": "Vehicle.Speed", "value": "20", "requestId":"sddf"}''')
        rep = await websocket.recv()
        print(f"<<< {rep}")


        print("SEEEEEEEEEET")

        await websocket.send('''{"action": "set"}''')
        rep = await websocket.recv()
        print(f"<<< {rep}")

        await websocket.send('''{"action": "set", "path": "Vehicle.Speed", "requestId":"sddf"}''')
        rep = await websocket.recv()
        print(f"<<< {rep}")

        await websocket.send('''{"action": "set", "path": "Vehicle.Speed", "value": "400", "authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJsb2NhbCBkZXYiLCJpc3MiOiJjcmVhdGVUb2tlbi5weSIsImF1ZCI6WyJrdWtzYS52YWwiXSwiaWF0IjoxNTE2MjM5MDIyLCJleHAiOjE3NjcyMjU1OTksInNjb3BlIjoicmVhZDpWZWhpY2xlLldpZHRoIHByb3ZpZGU6VmVoaWNsZS5TcGVlZCJ9.w2c8xrYwBVgMav3f0Se6E8H8E36Nd03rJiSS2A8s-CL3GtlwB7wVanjXHhppNsCdWym3tK4JwgslQdMQF-UL4hd7vzdtt-Mx6VjH_jO9mDxz4Z0Uzw7aJtbtQSpi2h6kwceTVTllkbLRF7WRHWIpwzXFF9yZolX6lH-BE9xf1AB62d6icd9SKxFnVvYs3MVK5D1xNmDNOmm-Fr0d2K604MmIIXGW5kPZJYIvBKO4NYRLklhJe47It_lGo3gnh1ppmzTOIo1kB4sDe55hplUCbTCJVricpyQSgTYsf7aFRPK51XMRwwwJ8kShWeaTggMLKpv1W-9dhVWDk4isC8BxsOjaVloArausMmjLmTz6KwAsfARgfXtaCrMsESUBNXi5KIdAyHVXZpmERvc9yeYPcaWlknVFrFsHbV6bw4nwqBX-0Ubuga0NGNQDFKmyTKQrbuZmQ3L9iipxY8_BOSCkdiYtWbE3lpplxpS_PaZl10KAaMmUfbcF9aYZunDEzEtoJgJe2EeGu3XDBtbyXVUKruImdSEdjaImfUGQIWl5bMbVH4N4zK5jE45wT5FJiRUcA5pMN5wNmDYJJzgbxWNpYW40KZYPFc_7XUH8EZ2Cs69wDHam3ArkOs1qMgMIoEPWVzHakjlVJfrPR9zQKxfirBtNNENIoHsBjJ_P4FEJCN4", "requestId":"sddf"}''')
        rep = await websocket.recv()
        print(f"<<< {rep}")

        print("Subscribe test")
        await websocket.send('''{"action": "subscribe"}''')
        rep = await websocket.recv()
        print(f"<<< {rep}")

        await websocket.send('''{"action": "subscribe", "path": "Vehicle.NotExist", "requestId":"sddf"}''')
        while True:
            rep = await websocket.recv()
            print(f"<<< {rep}")
            if "error" in rep:
                break

        await websocket.send('''{"action": "subscribe", "path": "Vehicle.Speed", "requestId":"sddf"}''')
        while True:
            rep = await websocket.recv()
            print(f"<<< {rep}")
            if "error" in rep:
                break

if __name__ == "__main__":
    asyncio.run(hello())
