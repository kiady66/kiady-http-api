from src.login import check_user_token
from src.send_response import send_response
from src.request_db import request_db
from src.request_db import update_db
from src.static_function import convert_json_to_array
from src.static_function import str_to_dtime
from src.static_function import extract_task_from_request
from src.static_function import get_user


# TODO: add flexible_id attribute to task in db


def get_task(event, context):
    request_script = f"SELECT * FROM task WHERE %s=ANY(admins)"
    user_id = int(get_user(event)["id"])
    return send_response(request_db(request_script, [user_id]), 200)


# TODO: validation (check if start_date < end_date)
# TODO: modify (drop/insert) flexible task in db
# TODO: validation (check if all the tasks sent are not overlapping) : not compare
def create_task(event, context):
    return update_tasks(event, insert_task_to_db, is_creating_task=True)


# TODO: validation (check if start_date < end_date)
# TODO: modify (drop/insert) flexible task in db
def update_task(event, context):
    update_tasks(event, update_task_to_db)


def delete_task(event, context):
    update_tasks(event, delete_task_to_db, True)


def insert_task_to_db(tasks):
    for task in tasks:
        insert_script = ' INSERT INTO task (name, admins, users, type, configuration, priority, start_date, end_date, duration) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
        insert_value = (
            task["name"], convert_json_to_array(task["admins"]),
            convert_json_to_array(task["users"]), task["type"],
            task["configuration"], task["priority"],
            str_to_dtime(task["start_date"]), str_to_dtime(task["end_date"]),
            task["duration"]
        )
        update_db(insert_script, insert_value)


def update_task_to_db(tasks):
    for task in tasks:
        update_script = 'UPDATE task SET (name, admins, users, type, configuration, priority, start_date, end_date, duration, pinned) = (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) where id = %s'
        update_values = (
            task["name"], convert_json_to_array(task["admins"]),
            convert_json_to_array(task["users"]), task["type"],
            task["configuration"], task["priority"],
            str_to_dtime(task["start_date"]), str_to_dtime(task["end_date"]),
            task["duration"], convert_json_to_array(task["pinned"]), task["task_id"]
        )
        update_db(update_script, update_values)
    #check if the task is flexible
    #if it is flexible, delete all the flexible task with the same flexible_id and insert the new one
    #while inserting, calculate the new flexible_id
    #report if there is no place for the flexible task
    #propose user to reduce the duration of the flexible task
    #propose user to reduce the duration of one of the task that overlap with the flexible task



def delete_task_to_db(tasks):
    for task in tasks:
        delete_script = 'DELETE FROM task where id = %s'
        delete_values = task["task_id"]
        request_db.update_db(delete_script, delete_values)


def is_owner(tasks, user_id):
    for task in tasks:
        request_script = 'SELECT * from task where id = %s AND %s =ANY(admins);'
        request_value = (task["task_id"], user_id)
        if not request_db(request_script, request_value):
            return False
    return False


# return list of task that overlap
def check_overlaps(tasks):
    request_script = 'SELECT * FROM task where '
    request_value = ()
    length = len(tasks) - 1
    i = 0

    for task in tasks:
        request_script = request_script + 'start_date between %s and %s or end_date between %s and %s'
        request_value = request_value + (
            str_to_dtime(task["start_date"]),
            str_to_dtime(task["end_date"]),
            str_to_dtime(task["start_date"]),
            str_to_dtime(task["end_date"])
        )
        if i < length:
            request_script = request_script + ' or '
            i += 1

    return request_db(request_script, request_value)


# The variable "delete_call_back" is none if update_tasks is not a deleting function
def update_tasks(event, callback, is_deleting_task=False, is_creating_task=False):
    if not check_user_token(event):
        return send_response("access error", 403)

    if not is_creating_task:
        if not is_owner(extract_task_from_request(event), get_user(event)["id"]):
            return send_response("access error", 403)

    if not is_deleting_task:
        try:
            overlapping = check_overlaps(extract_task_from_request(event))
        except Exception:
            return send_response("something went wrong")
        if overlapping:
            return send_response({
                "tasks_overlapping": overlapping,
            }, 200)

    try:
        callback(extract_task_from_request(event))
        return send_response("success", 200)
    except:
        send_response("internal error", 500)
