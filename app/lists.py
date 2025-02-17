from flask import Blueprint, render_template
from flask_login import current_user, login_required
from .models.Task import Task
from .models.List import List

lists = Blueprint("lists", __name__)


@lists.route("/")
@login_required
def index():
    lists = List.query.all()
    return render_template("lists/index.html", user=current_user, lists=lists)


@lists.route("/lists/<int:list_id>/add_task/<task_name>", methods=["GET", "POST"])
@login_required
def add_task(list_id, task_name):
    task = Task.query.filter_by(name=task_name).first()
    list = List.query.get(list_id)
    list.tasks.append(task)
    list.save()
    return {"status": "success"}, 200


@lists.route("/lists/<int:list_id>/tasks", methods=["GET"])
@login_required
def get_tasks(list_id):
    list = List.query.get(list_id)
    tasks = list.tasks
    tasks_dict = []
    for task in tasks:
        status = task.get_task_status(task.id, list.id)
        task_dict = task.to_dict()
        task_dict["status"] = status
        tasks_dict.append(task_dict)
    return {"tasks": tasks_dict}, 200


@lists.route(
    "/lists/<int:list_id>/tasks/<task_name>/toggle_status", methods=["GET", "POST"]
)
@login_required
def toggle_task_status(list_id, task_name):
    list = List.query.get(list_id)
    task = Task.query.filter_by(name=task_name).first()
    Task.toggle_task_status(list.id, task.id)
    return {"status": "success"}, 200
