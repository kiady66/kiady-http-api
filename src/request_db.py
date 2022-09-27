import os

import psycopg2

hostname = os.environ["HOST_NAME"]
database = os.environ["DB_NAME"]
username = os.environ["USERNAME"]
pwd = os.environ["PASSWORD"]
port_id = os.environ["PORT"]
connection = None
cursor = None


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


def request_db(request_script, request_value):
    try:
        connection = psycopg2.connect(
            host=hostname,
            dbname=database,
            user=username,
            password=pwd,
            port=port_id
        )

        cursor = connection.cursor()

        cursor.execute(request_script, request_value)
        r = [dict((cursor.description[i][0], value) \
                  for i, value in enumerate(row)) for row in cursor.fetchall()]
        one = False

        print(r)

        return (r[0] if r else None) if one else r

    except Exception as error:
        print(error)
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()
