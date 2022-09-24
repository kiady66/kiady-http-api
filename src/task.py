import json
from src.login import login
from src.send_response import send_response
from src.request_db import request_db
from src.request_db import update_db
from src.static_function import convert_json_to_array
from src.static_function import str_to_dtime
from src.static_function import test


# TODO: add flexible_id attribute to task in db
def create_task(event, context):

    # TODO: check if user own the task
    # TODO: check if task has to be override

    try:
        insert_task_to_db(event)
        return send_response("success", 200)
    except:
        return send_response("internal error", 500)


def update_task(event, context):
    if not login.check_user_token(event):
        return send_response("access error", 403)

    # TODO: check if user own the task
    # TODO: check if task has to be override (only warn front)

    try:
        update_task_to_db(event)
        return send_response("success", 200)
    except:
        return send_response("internal error", 500)


def delete_task(event, context):
    if not login.check_user_token(event):
        return send_response("access error", 403)

    # TODO: check if user own the task
    # TODO: check if task has to be override (only warn front)

    try:
        delete_task_to_db(event)
        send_response("success", 200)
    except:
        send_response("internal error", 500)


def insert_task_to_db(event):
    parameters = json.loads(event["body"])
    insert_script = ' INSERT INTO task (name, admins, users, type, configuration, priority, start_date, end_date, duration) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
    insert_value = (
        parameters["name"], convert_json_to_array(parameters["admins"]),
        convert_json_to_array(parameters["users"]), parameters["type"],
        parameters["configuration"], parameters["priority"],
        str_to_dtime(parameters["start_date"]), str_to_dtime(parameters["end_date"]),
        parameters["duration"]
    )
    update_db(insert_script, insert_value)


def update_task_to_db(event):
    parameters = json.loads(event["body"])
    update_script = 'UPDATE task SET (name, admins, users, type, configuration, priority, start_date, end_date, duration, pinned) = (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) where id = %s'
    update_values = (
        parameters["name"], convert_json_to_array(parameters["admins"]),
        convert_json_to_array(parameters["users"]), parameters["type"],
        parameters["configuration"], parameters["priority"],
        str_to_dtime(parameters["start_date"]), str_to_dtime(parameters["end_date"]),
        parameters["duration"], convert_json_to_array(parameters["pinned"]), parameters["task_id"]
    )
    update_db(update_script, update_values)


def delete_task_to_db(event):
    parameters = json.loads(event["body"])
    delete_script = 'DELETE FROM task where id = %s'
    delete_values = parameters["task_id"]
    request_db.update_db(delete_script, delete_values)


def is_owner(tasks, user_id):
    for task in tasks:
        request_script = 'SELECT * from task where id = %s AND %s =ANY(admins);'
        request_value = (task["task_id"], user_id)
        if not request_db(request_script, request_value):
            return False
    return False
