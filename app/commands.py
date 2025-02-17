import click
from flask import Blueprint
from .models.List import List
from .models.User import User


commands = Blueprint("commands", __name__)


@commands.cli.command("create_user")
@click.argument("username")
@click.argument("password")
def create_user(username, password):
    user = User(username, password)
    user.save()


@commands.cli.command("create_list")
@click.argument("name")
def create_list(name):
    user = User.query.first()
    list = List(name, user)
    list.save()
