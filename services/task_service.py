from asyncio import Task
from repositories.task_repository import TaskRepository

class TaskService:

    @staticmethod
    def list_all_tasks(user_id: int):
        tasks = TaskRepository.get_all(user_id)
        return [task.to_dict() for task in tasks]

    @staticmethod
    def create_task(data: dict, user_id: int):

        title = data.get("title")

        if not title or not title.strip():
            raise ValueError("O título da tarefa é obrigatório.")

        description = data.get("description", "").strip()

        return TaskRepository.create(
            title=title.strip(),
            description=description,
            user_id=user_id
        ).to_dict()

    @staticmethod
    def update_task(task_id: int, data: dict, user_id: int):
        task = TaskRepository.get_by_id(task_id)
        if not task:
            return None

        # Check if the user is the owner of the task
        if task.user_id != user_id:
            raise ValueError("Você não tem permissão para atualizar esta tarefa.")

        title = data.get("title")
        description = data.get("description")
        completed = data.get("completed")

        if title is not None and not title.strip():
            raise ValueError("O título não pode ser vazio.")

        updated_task = TaskRepository.update(
            task, 
            title=title.strip() if title else None,
            description=description.strip() if description is not None else None,
            completed=completed
        )
        return updated_task.to_dict()

    @staticmethod
    def delete_task(task_id: int, user_id: int):
        task = TaskRepository.get_by_id(task_id)
        if not task:
            return False

        # Check if the user is the owner of the task
        if task.user_id != user_id:
            raise ValueError("Você não tem permissão para excluir esta tarefa.")

        TaskRepository.delete(task)
        return True