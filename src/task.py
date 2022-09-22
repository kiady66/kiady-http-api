import json
import login
import send_response
import update_db


def create_task(event, context):
    if not login.check_user_token(event):
        return send_response.send_response("access error", 403)

    # TODO: check if user own the task

    try:
        insert_task_to_db(event)
        send_response.send_response("success", 200)
    except:
        send_response.send_response("internal error", 500)


def update_task(event, context):
    if not login.check_user_token(event):
        return send_response.send_response("access error", 403)

    # TODO: check if user own the task

    try:
        update_task_to_db(event)
        send_response.send_response("success", 200)
    except:
        send_response.send_response("internal error", 500)


def delete_task(event, context):
    if not login.check_user_token(event):
        return send_response.send_response("access error", 403)

    # TODO: check if user own the task

    try:
        delete_task_to_db(event)
        send_response.send_response("success", 200)
    except:
        send_response.send_response("internal error", 500)


def insert_task_to_db(event):
    parameters = json.loads(event["body"])
    insert_script = ' INSERT INTO task (name, admins, users, type, configuration, priority, start_date, end_date, duration) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
    insert_value = (
        parameters["name"], parameters["admin"],
        parameters["users"], parameters["type"],
        parameters["configuration"], parameters["priority"],
        parameters["start_date"], parameters["end_date"],
        parameters["duration"]
    )
    update_db(insert_script, insert_value)


def update_task_to_db(event):
    parameters = json.loads(event["body"])
    update_script = 'UPDATE task SET (name, admins, users, type, configuration, priority, start_date, end_date, duration) = (%s, %s, %s, %s, %s, %s, %s, %s, %s) where id = %s'
    update_values = (
        parameters["name"], parameters["admins"],
        parameters["users"], parameters["type"],
        parameters["configuration"], parameters["priority"],
        parameters["start_date"], parameters["end_date"],
        parameters["duration"], parameters["id"]
    )
    update_db(update_script, update_values)


def delete_task_to_db(event):
    parameters = json.loads(event["body"])
    delete_script = 'DELETE FROM task where id = %s'
    delete_values = parameters["id"]
    update_db(delete_script, delete_values)
