import json
import os

import firebase_admin
from firebase_admin import auth
from firebase_admin import credentials
from src.request_db import update_db


def login(event, context):
    if not check_user_token(event):
        return {
            'statusCode': 401,
            'body': json.dumps('Unauthorized')
        }

    parameters = json.loads(event["body"])
    insert_user_to_db(parameters["username"], parameters["email"], parameters["udid"])
    response = {"statusCode": 200, "body": json.dumps('Connected')}

    return response


def insert_user_to_db(user_name, email, udid):
    insert_script = ' INSERT INTO "user" (username, email, udid) VALUES (%s, %s, %s)'
    insert_value = (user_name, email, udid)
    update_db(insert_script, insert_value)


def check_user_token(event):
    if os.environ['APP_ENV'] == 'dev':
        return True
    try:
        parameters = json.loads(event["body"])
        token_id = parameters["id_token"]

        cred = credentials.Certificate("src/serviceAccountKey.json")
        firebase_admin.initialize_app(cred)

        decoded_token = auth.verify_id_token(token_id)
        if decoded_token['uid']:
            return True
        else:
            return False
    except Exception:
        return False
