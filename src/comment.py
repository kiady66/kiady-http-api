import json
import psycopg2
from firebase_admin import auth

hostname = 'localhost'
database = 'personal_calendar'
username = 'postgres'
pwd = 'root'
port_id = 5432
connection = None
cursor = None


def send_response(event, context):
    body = {
        "message": "Hello word",
        "input": event
    }

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response


def insert_comment_to_db(event, context):
    # check if user is connected
    parameters = json.loads(event["body"])
    sender = parameters["sender"], content = parameters["content"], date = parameters["date"]
    insert_script = 'INSERT INTO "comment" (sender, content, date) VALUES (%s, %s, %s)'
    insert_value = (sender, content, date)
    update_db(insert_script, insert_value)
    send_response(event, context)


def update_comment_to_db(id, content):
    # check if user is connected and user_id = sender
    update_script = 'UPDATE "comment" SET content = %s where id = %s'
    update_values = (content, id)
    update_db(update_script, update_values)


def delete_comment_to_db(id):
    # check if user is connected and user_id = sender
    delete_script = 'DELETE FROM "comment" where id = %s'
    delete_values = id


def update_db(insert_script, insert_value):
    try:
        connection = psycopg2.connect(
            host=hostname,
            dbname=database,
            user=username,
            password=pwd,
            port=port_id
        )

        cursor = connection.cursor()

        cursor.execute(insert_script, insert_value)
        connection.commit()

    except Exception as error:
        print(error)
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()

def test(event, context):
    parameters = json.loads(event["body"])
    token_id = parameters["id_token"]

    decoded_token = auth.verify_id_token(token_id)
    uid = decoded_token['uid']

    print(uid)