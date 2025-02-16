from flask import Blueprint, request
from flask_login import login_required
from .models.Task import Task

tasks = Blueprint("tasks", __name__)


@tasks.route("/")
@login_required
def get_all_tasks():
    tasks = Task.query.all()
    tasks = [task.to_dict() for task in tasks]
    return {"tasks": tasks}, 200


@tasks.route("/", methods=["POST"])
@login_required
def create_task():
    task = Task(name=request.json.get("name"))
    task.save()
    return {"status": "success"}, 200
