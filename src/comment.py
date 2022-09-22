import json
import update_db
import send_response
import login


def create_comment(event, context):
    if not login.check_user_token(event):
        return send_response.send_response("access error", 403)

    # TODO: check if user own the comment

    try:
        insert_comment_to_db(event)
        send_response.send_response("success", 200)
    except:
        send_response.send_response("internal error", 500)


def update_comment(event, context):
    if not login.check_user_token(event):
        return send_response.send_response("access error", 403)

    # TODO: check if user own the comment

    try:
        update_comment_to_db(event)
        send_response.send_response("success", 200)
    except:
        send_response.send_response("internal error", 500)


def delete_comment(event, context):
    if not login.check_user_token(event):
        return send_response.send_response("access error", 403)

    # TODO: check if user own the comment

    try:
        delete_comment_to_db(event)
        send_response.send_response("success", 200)
    except:
        send_response.send_response("internal error", 500)


def insert_comment_to_db(event, context):
    parameters = json.loads(event["body"])
    insert_script = 'INSERT INTO "comment" (sender, content, date) VALUES (%s, %s, %s)'
    insert_value = (parameters["sender"], parameters["content"], parameters["date"])
    update_db.update_db(insert_script, insert_value)


def update_comment_to_db(event):
    parameters = json.loads(event["body"])
    update_script = 'UPDATE "comment" SET content = %s where id = %s'
    update_values = (parameters["content"], parameters["comment_id"])
    update_db.update_db(update_script, update_values)


def delete_comment_to_db(event):
    parameters = json.loads(event["body"])
    delete_script = 'DELETE FROM "comment" where id = %s'
    delete_values = parameters["comment_id"]
    update_db.update_db(delete_script, delete_values)
