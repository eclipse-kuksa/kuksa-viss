import json

def createVISSV2Error(number, reason, message):
    msg={}
    msg["error"]={}
    msg["error"]["number"]=number
    msg["error"]["reason"]=reason
    msg["error"]["message"]=message
    return json.dumps(msg)

def create_badrequest_error(message):
    return createVISSV2Error(400, "bad_request", message)
