import asyncio
import websockets
import json
import errorhelper as err
import vissv2impl
import argparse

from kuksa_client.grpc.aio import VSSClient


async def vissv2(websocket):
    global dbhost, dbport
    if websocket.subprotocol != "VISSv2":
        if websocket.subprotocol is not None:
            await websocket.close(reason=f"Unsupported subprotocol {websocket.subprotocol} ")
            return
        print("Warning: No subprotocol selected. Moving on, but a well-behaved client shall set subprotocol to VISSv2")

    print(f"Connecting to databroker at {dbhost} port {dbport}")
    kuksa = VSSClient(dbhost, dbport)
    try:
        await kuksa.connect()
    except Exception as exp:
        print(f"Not connection to KUKSA databroker: {exp}")
        return

    while True:
        msg = ""
        try:
            msg = await websocket.recv()
        except websockets.exceptions.ConnectionClosed:
            print("Client closed the connection")
            return

        print(f"RX {msg}")
        try:
            msgObj = json.loads(msg)
            await vissv2impl.process_request(websocket, kuksa, msgObj, provideEnable)
        except json.JSONDecodeError as exp:
            await websocket.send(err.create_badrequest_error(f"The request is not valid JSON:{exp}"))
        except Exception as exp:
            print(f"Bad things:{exp}")
            await websocket.send(err.createVISSV2Error(500, "internal_error", "Unexpected error during processing"))

        print("Processing done")


async def main(args):
    print(f"Listening on port {args.port}")
    print(f"Will use {args.dbhost} port {args.dbport} for databroker connection")
    async with websockets.serve(vissv2, "127.0.0.1", args.port, subprotocols=["VISSv2"]):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    global dbhost
    global dbport
    global provideEnable
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--dbhost', help="KUKSA databroker host", default="localhost")
    parser.add_argument(
        '--dbport', type=int, help="KUKSA databroker port", default=55555)
    parser.add_argument(
        '--port', type=int, help="VISS websocket port", default=8090)
    parser.add_argument(
        '--provide', type=bool, help="enable provide for VISS interface, should not be in VISS per definition but for usability we can enable it", default=False)
    args = parser.parse_args()
    dbhost = args.dbhost
    dbport = args.dbport
    provideEnable = args.provide

    asyncio.run(main(args))
