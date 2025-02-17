from flask import Blueprint, request
from flask_login import login_required
from .models.Task import Task
from .models.List import List
from .models.User import User


commands = Blueprint("commands", __name__)


@commands.cli.command("create_user")
def create_user():
    user = User("test@gmail.com", "test", "password")
    user.save()


@commands.cli.command("create_list")
def create_list():
    user = User.query.first()
    list = List("test", user)
    list.save()
