import json
import time
import uuid

def generate_json(code, message, data):
    return {
        "code": code,
        "time":  int(time.time()),
        "uuid": str(uuid.uuid4()),
        "message": message,
        "data": data
    }

def generate_jsonstr(code, message, data):
    return json.dumps(generate_json(code, message,data))
