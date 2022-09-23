import psycopg2

hostname = 'localhost'
database = 'personal_calendar'
username = 'postgres'
pwd = 'root'
port_id = 5432
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

        return cursor.fetchall()

    except Exception as error:
        print(error)
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()
