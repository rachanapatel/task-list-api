from flask import Blueprint, request, abort, make_response, Response
from app.models.goal import Goal
from ..db import db
# from app.routes.task_routes import validate_task
from .route_utilities import validate_model, create_model
from app.models.task import Task



goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@goals_bp.post("")
def create_tasks():
    request_body = request.get_json()
    return {"goal": create_model(Goal, request_body)[0]}, 201
    # try:
    #     new_goal = Goal.from_dict(request_body)
    # except KeyError as error:
    #     response_body = {"details": "Invalid data"}
    #     abort(make_response(response_body, 400))

    # db.session.add(new_goal)
    # db.session.commit()
    # response = {"goal": new_goal.to_dict()}
    # return response, 201

@goals_bp.get("")
def get_all_goals():
    query = db.select(Goal)

    # sort_param = request.args.get("sort")
    # if sort_param == "asc":
    #     query = query.order_by(Goal.title.asc())
    # if sort_param == "desc":
    #     query = query.order_by(Goal.title.desc())

    # tasks = db.session.scalars(query.order_by(Task.id))
    goals = db.session.execute(query).scalars()

    goals_response = []
    for goal in goals:
        goals_response.append(goal.to_dict())
    return goals_response



@goals_bp.get("/<goal_id>")
def get_one_goal(goal_id):
    # goal = validate_goal(goal_id)
    goal = validate_model(Goal, goal_id)
    response = {"goal": goal.to_dict()}
   
    return response



# def validate_goal(goal_id):
#     query = db.select(Goal).where(Goal.id == goal_id)
#     goal = db.session.scalar(query)

#     if not goal:
#         response = {"message": f"Goal {goal_id} not found"}
#         abort(make_response(response, 404))

#     return goal 

@goals_bp.put("/<goal_id>")
def update_goal(goal_id):
    # goal = validate_goal(goal_id)
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    goal.title = request_body["title"]
    goal.id = request_body["id"]
    db.session.commit()
    return Response(status=204, mimetype="application/json")


@goals_bp.delete("/<goal_id>")
def delete_goal(goal_id):
    # goal = validate_goal(goal_id)
    goal = validate_model(Goal, goal_id)
    db.session.delete(goal)
    db.session.commit()
    return Response(status=204, mimetype="application/json")

@goals_bp.get("/<goal_id>/tasks")
def get_tasks_by_goal(goal_id):
    # goal = validate_goal(goal_id)
    goal = validate_model(Goal, goal_id)
    response = goal.to_dict()
    response["tasks"] = [task.to_dict() for task in goal.tasks]
    return response

@goals_bp.post("/<goal_id>/tasks")
def send_tasks_to_goals(goal_id):
    # goal = validate_goal(goal_id)
    goal = validate_model(Goal, goal_id)
    
    request_body = request.get_json()
    task_list = request_body["task_ids"]
    goal.tasks.clear() #removes existing tasks assoc w the goal

    for task_id in request_body["task_ids"]:
        new_task = validate_model(Task, task_id)
        new_task.goal_id = goal_id

    db.session.commit()
    response = {"id": goal.id, 
                "task_ids": request_body["task_ids"]}

    return response