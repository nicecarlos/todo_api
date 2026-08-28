from extensions import db
from models.task import Task

class TaskRepository:

    @staticmethod
    def get_all():
        return Task.query.order_by(Task.created_at.desc()).all()

    @staticmethod
    def get_by_id(task_id: int):
        return Task.query.get(task_id)

    @staticmethod
    def create(title: str, description: str = None):
        task = Task(title=title, description=description)
        db.session.add(task)
        db.session.commit()
        return task

    @staticmethod
    def update(task: Task, title: str = None, description: str = None, completed: bool = None):
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if completed is not None:
            task.completed = completed
        
        db.session.commit()
        return task

    @staticmethod
    def delete(task: Task):
        db.session.delete(task)
        db.session.commit()