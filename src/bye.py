import json


def by(event, context):
    body = {
        "message": "Bye word",
    }

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response
