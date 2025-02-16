from flask import Blueprint, render_template
from flask_login import current_user, login_required
from .models.Task import Task
from .models.List import List

lists = Blueprint("lists", __name__)


@lists.route("/")
@login_required
def index():
    return render_template(
        "lists/index.html", user=current_user, lists=List.query.all()
    )


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
    tasks = [task.to_dict() for task in tasks]
    return {"tasks": tasks}, 200
