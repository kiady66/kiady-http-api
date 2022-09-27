import json


def send_response(message, status_code):
    body = {
        "message": message
    }
    response = {"statusCode": status_code, "body": json.dumps(body, default=str)}
    return response
