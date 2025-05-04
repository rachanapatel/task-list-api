from flask import Blueprint, request, abort, make_response, Response
from app.models.task import Task
from ..db import db
from datetime import datetime


tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@tasks_bp.post("")
def create_tasks():
    request_body = request.get_json()
   
    try:
        new_task = Task.from_dict(request_body)
    except KeyError as error:
        response_body = {"details": "Invalid data"}
        abort(make_response(response_body, 400))

    db.session.add(new_task)
    db.session.commit()
    response = {"task": new_task.task_dict()}
    return response, 201


@tasks_bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_task(task_id)
    response = {"task": task.task_dict()}
   
    return response



def validate_task(task_id):
    query = db.select(Task).where(Task.id == task_id)
    task = db.session.scalar(query)

    if not task:
        response = {"message": f"Task {task_id} not found"}
        abort(make_response(response, 404))

    return task 



@tasks_bp.get("")
def get_all_tasks():
    query = db.Select(Task)

    sort_param = request.args.get("sort")
    if sort_param == "asc":
        query = query.order_by(Task.title.asc())
    if sort_param == "desc":
        query = query.order_by(Task.title.desc())

    # tasks = db.session.scalars(query.order_by(Task.id))
    tasks = db.session.execute(query).scalars()

    tasks_response = []
    for task in tasks:
        tasks_response.append(task.task_dict())
    return tasks_response


@tasks_bp.put("/<task_id>")
def update_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]
    db.session.commit()
    return Response(status=204, mimetype="application/json")

@tasks_bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_task(task_id)
    db.session.delete(task)
    db.session.commit()
    return Response(status=204, mimetype="application/json")


@tasks_bp.patch("/<task_id>/mark_complete")
def mark_complete(task_id):
    task = validate_task(task_id)

    task.completed_at = datetime.now()
    
    if task.completed_at:
        task.is_complete = True

    db.session.commit()


    return Response(status=204, mimetype="application/json")


@tasks_bp.patch("/<task_id>/mark_incomplete")
def mark_incomplete(task_id):
    task = validate_task(task_id)

    task.completed_at = None
    
    db.session.commit()

    return Response(status=204, mimetype="application/json")