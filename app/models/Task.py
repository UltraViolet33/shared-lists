from .. import db
from .Model import Model


class Task(db.Model, Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False)

    lists = db.relationship(
        "List",
        secondary="lists_tasks",
        back_populates="tasks",
    )

    def __init__(self, name):
        self.name = name

    def to_dict(self):
        return self.name


    def toggle_status(self):
        self.status = not self.status
        return self.status
