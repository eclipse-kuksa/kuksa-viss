import asyncio
import websockets
import json
import errorhelper as err
import vissv2impl

from kuksa_client.grpc.aio import VSSClient




async def vissv2(websocket):
    if websocket.subprotocol != "VISSv2":
        if websocket.subprotocol != None:
            await websocket.close(reason=f"Unsupported subprotocol {websocket.subprotocol} ")
            return
        print("Warning: No subprotocol selected. Moving on, but a well-behaved client shall set subprotocol to VISSv2")
    
    kuksa=VSSClient('127.0.0.1', 55557)
    try:
        await kuksa.connect()
    except Exception as exp:
        print(f"Not connection to KUKSA databroker: {exp}")
        return

    while True:
        msg=""
        try:
            msg = await websocket.recv()
        except websockets.exceptions.ConnectionClosed:
            print("Client closed the connection")
            return
        
        print(f"RX {msg}")
        try:
            msgObj = json.loads(msg)
            await vissv2impl.process_request(websocket, kuksa, msgObj)
        except json.JSONDecodeError as exp:
             await websocket.send(err.create_badrequest_error(f"The request is not valid JSON:{exp}"))
        except Exception as exp:
            print(f"Bad things:{exp}")
            await websocket.send(err.createVISSV2Error(500, "internal_error", "Unexpected error during processing"))

        print("Processing done")
    
        
async def main():
    async with websockets.serve(vissv2, "localhost", 8765, subprotocols=["VISSv2"]):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())