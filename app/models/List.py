from .. import db
from .Model import Model


class List(db.Model, Model):
    __tablename__ = "lists"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = db.relationship("User", back_populates="lists")

    tasks = db.relationship(
        "Task",
        secondary="lists_tasks",
        back_populates="lists",
    )

    def __init__(self, name, user):
        self.name = name
        self.user = user
