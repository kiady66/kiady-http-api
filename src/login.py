import json
import psycopg2



hostname = 'localhost'
database = 'personal_calendar'
username = 'postgres'
pwd = 'root'
port_id = 5432
connection = None
cursor = None

def login(event, context):

    body = {
        "message": "Hello word",
        "input": event
    }

    parameters = json.loads(event["body"])

    insert_user(parameters["username"], parameters["email"], parameters["udid"])

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response


def insert_user(user_name, email, udid):

    try:
        connection = psycopg2.connect(
            host = hostname,
            dbname = database,
            user = username,
            password = pwd,
            port = port_id
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

