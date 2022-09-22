import json
import psycopg2
import firebase_admin
from firebase_admin import auth
from firebase_admin import credentials


hostname = 'localhost'
database = 'personal_calendar'
username = 'postgres'
pwd = 'root'
port_id = 5432
connection = None
cursor = None


def login(event, context):
    parameters = json.loads(event["body"])


    insert_user(parameters["username"], parameters["email"], parameters["udid"])

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response


def insert_user(user_name, email, udid):
    try:
        connection = psycopg2.connect(
            host=hostname,
            dbname=database,
            user=username,
            password=pwd,
            port=port_id
        )

        cursor = connection.cursor()

        insert_script = ' INSERT INTO "user" (username, email, udid) VALUES (%s, %s, %s)'
        insert_value = (user_name, email, udid)

        cursor.execute(insert_script, insert_value)
        connection.commit()

    except Exception as error:
        print(error)
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()


def check_user_token(event):
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
    except:
        return False

