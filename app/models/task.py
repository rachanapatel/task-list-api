from sqlalchemy.orm import Mapped, mapped_column
from ..db import db
from datetime import datetime

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[datetime] = mapped_column(default=None, nullable=True)
    is_complete: Mapped[bool] = mapped_column(default=False)

    def task_dict(self):
        task_as_dict = {}
        task_as_dict["id"] = self.id
        task_as_dict["title"] = self.title
        task_as_dict["description"] = self.description
        task_as_dict["is_complete"] = self.is_complete
        return task_as_dict


    @classmethod
    def from_dict(cls, task_data):
        new_task = cls(title=task_data["title"],
                       description=task_data["description"])
        return new_task
