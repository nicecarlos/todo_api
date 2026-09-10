from extensions import db
from models.task import Task

class TaskRepository:

    @staticmethod
    def get_all(user_id: int):
        return Task.query.filter(Task.user_id == user_id).all()

    @staticmethod
    def get_by_id(task_id: int):
        return Task.query.get(task_id)

    @staticmethod
    def create(title: str, description: str, user_id: int):
        task = Task(
            title=title,
            description=description,
            user_id=user_id
        )

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
