import uuid
import errorhelper as err
import datapointhelper as dp

import json
from jsonschema import ValidationError, Draft202012Validator, RefResolver

from datetime import datetime

from kuksa_client.grpc import VSSClientError, Datapoint


vissresolver = RefResolver.from_schema(
    schema={"title": "Vissv2 stuff"},
    store={"vissv2base": {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "definitions": {
            "requestId": {
                "description": "Returned by the server in the response and used by the client to link the request and response messages.",
                "type": "string"
            },
            "path": {
                "description": "The path to the desired vehicle signal(s), as defined by the metadata schema.",
                "type": "string"
            },
            "authorization": {
                "description": "Token to be used for this request",
                "type": "string"
            },
        }
    }},
)


GET_SCHEMA = json.loads("""
{
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "Get Request",
    "description": "Get the value of one or more vehicle signals and data attributes",
    "type": "object",
    "required": ["action", "path", "requestId" ],
    "properties": {
        "action": {
            "enum": [ "get" ],
            "description": "The identifier for the get request"
        },
        "path": {
            "$ref": "vissv2base#/definitions/path"
        },
        "requestId": {
            "$ref": "vissv2base#/definitions/requestId"
        },
        "authorization": {
            "$ref": "vissv2base#/definitions/authorization"
        },
        "filter": {
            "description": "May be specified in order to throttle the demands of subscriptions on the server. See [[viss2-core]], Filter Request chapter.",
            "type": "object",
            "properties": {
                "type": {
                    "description": "The different filter types.",
                    "type": "string"
                },
                "parameter": {
                    "description": "Parameter(s) for the different filter types",
                    "type": "object"
                }
            }
        }
    }
}
""")

SET_SCHEMA = json.loads("""
{
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "Set Request",
    "description": "Enables the client to set one or more values once.",
    "type": "object",
    "required": ["action", "path", "requestId", "value"],
    "properties": {
        "action": {
            "enum": [ "set" ],
            "description": "The identifier for the set request"
        },
        "value": {
            "type": "string"
        },
        "path": {
            "$ref": "vissv2base#/definitions/path"
        },
        "authorization": {
            "$ref": "vissv2base#/definitions/authorization"
        },
        "requestId": {
            "$ref": "vissv2base#/definitions/requestId"
        }
    }
}
""")

SUBSCRIBE_SCHEMA = json.loads("""
{
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "Subscribe Request",
    "description": "Allows the client to subscribe to time-varying signal notifications on the server.",
    "type": "object",
    "required": ["action", "path", "requestId"],
    "properties": {
        "action": {
            "enum": [ "subscribe" ],
            "description": "The identifier for the subscription request"
        },
        "path": {
            "$ref": "vissv2base#/definitions/path"
        },
        "attribute": {
            "enum": [ "targetValue", "value" ],
            "description": "The attributes to be fetched for the get request"
        },
        "authorization": {
            "$ref": "vissv2base#/definitions/authorization"
        },
        "filters": {
            "$ref": "vissv2base#/definitions/filter"
        },
        "requestId": {
            "$ref": "vissv2base#/definitions/requestId"
        }
    }
}
""")


async def process_get(websocket, kuksa, msg):
    print("Process GET")
    try:
        validator = Draft202012Validator(GET_SCHEMA, resolver=vissresolver)
        validator.validate(msg)
    except ValidationError as exp:
        await websocket.send(err.create_badrequest_error(f"Invalid get request: {exp.message}"))
        return
    try:
        if "authorization" in msg:
            await kuksa.authorize(msg["authorization"])
        current_values = await kuksa.get_current_values([msg["path"]])
    except VSSClientError as exp:
        err_data = exp.to_dict()["error"]
        await websocket.send(err.createVISSV2Error(err_data["code"], err_data["reason"], err_data["message"]))
        return

    datapoints = dp.populate_datapoints(current_values)

    if not any(datapoints):
        await websocket.send(err.createVISSV2Error(404, "unavailable_data", "Currently no data available for your request"))
        return
    reply = {}
    reply["requestId"] = msg["requestId"]
    reply["action"] = "get"
    reply["data"] = datapoints

    await websocket.send(json.dumps(reply))


async def process_set(websocket, kuksa, msg):
    print("Process SET")
    try:
        validator = Draft202012Validator(SET_SCHEMA, resolver=vissresolver)
        validator.validate(msg)
    except ValidationError as exp:
        await websocket.send(err.create_badrequest_error(f"Invalid set request: {exp.message}"))
        return

    try:
        print("Setting targets")
        if "authorization" in msg:
            await kuksa.authorize(msg["authorization"])
        res = await kuksa.set_target_values({
            msg["path"]: Datapoint(msg["value"]),
        })
        print(f"Result is: {res} ")
    except VSSClientError as exp:
        err_data = exp.to_dict()["error"]
        await websocket.send(err.createVISSV2Error(err_data["code"], err_data["reason"], err_data["message"]))
        return

    # All good
    reply = {"action": "set", "requestId": msg["requestId"], "ts": datetime.now().isoformat(timespec="microseconds")}

    await websocket.send(json.dumps(reply))


async def process_subscribe(websocket, kuksa, msg):
    print("Process SUBSCRIBE")
    try:
        validator = Draft202012Validator(SUBSCRIBE_SCHEMA, resolver=vissresolver)
        validator.validate(msg)
    except ValidationError as exp:
        await websocket.send(err.create_badrequest_error(f"Invalid set request: {exp.message}"))
        return

    subscriptionId = str(uuid.uuid4())
    subscriptionReply = {"action": "subscribe", "requestId": msg["requestId"], "ts": datetime.now().isoformat(timespec="microseconds"), "subscriptionId": subscriptionId}
    await websocket.send(json.dumps(subscriptionReply))

    subscriptionReply["action"] = "subscription"

    try:
        if "authorization" in msg:
            await kuksa.authorize(msg["authorization"])
        async for update in kuksa.subscribe_current_values([
            msg['path']
        ]):
            print(f"Sub update: {update}")
            if msg['path'] in update and update[msg['path']] is not None:
                subscriptionReply["ts"] = datetime.now().isoformat(timespec="microseconds")
                subscriptionReply['data'] = dp.populate_datapoints(update)
                await websocket.send(json.dumps(subscriptionReply))
    except VSSClientError as exp:
        err_data = exp.to_dict()["error"]
        await websocket.send(err.createVISSV2Error(err_data["code"], err_data["reason"], err_data["message"]))
        return


async def process_request(websocket, kuksa, msg):
    if "action" not in msg:
        await websocket.send(err.create_badrequest_error("The request does not contain an action"))
        return

    if msg["action"] not in ["get", "set", "subscribe"]:
        await websocket.send(err.create_badrequest_error(f"Unknown action {msg['action']}"))
        return

    if msg["action"] == "get":
        await process_get(websocket, kuksa, msg)

    elif msg["action"] == "set":
        await process_set(websocket, kuksa, msg)

    elif msg["action"] == "subscribe":
        await process_subscribe(websocket, kuksa, msg)
