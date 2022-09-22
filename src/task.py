import json
import psycopg2


hostname = 'localhost'
database = 'personal_calendar'
username = 'postgres'
pwd = 'root'
port_id = 5432
connection = None
cursor = None

def create_task(event, context):
    body = {
        "message": "ok",
        "input": event
    }

    parameters = json.loads(event["body"])



def insert_task_to_db(name, admins, users, type, configuration, priority, start_date, end_date, duration):
    insert_script = ' INSERT INTO task (name, admins, users, type, configuration, priority, start_date, end_date, duration) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
    insert_value = (name, admins, users, type, configuration, priority, start_date, end_date, duration)
    update_db(insert_script, insert_value)


def update_task_to_db(id, name, admins, users, type, configuration, priority, start_date, end_date, duration):
    update_script = 'UPDATE task SET (name, admins, users, type, configuration, priority, start_date, end_date, duration) = (%s, %s, %s, %s, %s, %s, %s, %s, %s) where id = %s'
    update_values = (name, admins, users, type, configuration, priority, start_date, end_date, duration, id)

def delete_task_to_db(id):
    delete_script = 'DELETE FROM task where id = %s'
    delete_values = id

def update_db(insert_script, insert_value):
    try:
        connection = psycopg2.connect(
            host = hostname,
            dbname = database,
            user = username,
            password = pwd,
            port = port_id
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