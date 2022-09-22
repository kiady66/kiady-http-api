import json

import firebase_admin
from firebase_admin import auth
from firebase_admin import credentials


def test(event, context):
    parameters = json.loads(event["body"])
    token_id = parameters["id_token"]

    cred = credentials.Certificate("src/serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

    decoded_token = auth.verify_id_token(token_id)
    uid = decoded_token['uid']

    print(uid)
