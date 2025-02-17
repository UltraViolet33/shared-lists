from .. import db
from .Model import Model
from .List import List

lists_tasks = db.Table(
    "lists_tasks",
    db.Column("lists_id", db.Integer, db.ForeignKey("lists.id")),
    db.Column(
        "tasks_id",
        db.Integer,
        db.ForeignKey("tasks.id"),
    ),
    db.Column("status", db.Integer, nullable=False, default=0),
)


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
        return {
            "id": self.id,
            "name": self.name,
        }

    def get_task_status(self, task_id, list_id):
        entry = db.session.execute(
            db.select(lists_tasks).where(
                lists_tasks.c.lists_id == list_id, lists_tasks.c.tasks_id == task_id
            )
        ).fetchone()

        if entry:
            return entry.status

        return "Task not found in the list"

    @staticmethod
    def toggle_task_status(list_id, task_id):
        # Get the entry from the lists_tasks table
        entry = db.session.execute(
            db.select(lists_tasks).where(
                lists_tasks.c.lists_id == list_id, lists_tasks.c.tasks_id == task_id
            )
        ).fetchone()

        if entry:
            # Toggle the status (assuming 0 = incomplete, 1 = complete)
            new_status = 1 if entry.status == 0 else 0

            # Update the status
            db.session.execute(
                db.update(lists_tasks)
                .where(
                    lists_tasks.c.lists_id == list_id, lists_tasks.c.tasks_id == task_id
                )
                .values(status=new_status)
            )
            db.session.commit()
            return f"Task {task_id} in List {list_id} status toggled to {new_status}"

        return "Task not found in the list"
