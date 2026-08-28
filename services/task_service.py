from repositories.task_repository import TaskRepository

class TaskService:

    @staticmethod
    def list_all_tasks():
        tasks = TaskRepository.get_all()
        return [task.to_dict() for task in tasks]

    @staticmethod
    def create_task(data: dict):
        title = data.get("title")
        if not title or not title.strip():
            raise ValueError("O título da tarefa é obrigatório.")
        
        description = data.get("description", "").strip()
        return TaskRepository.create(title=title.strip(), description=description).to_dict()

    @staticmethod
    def update_task(task_id: int, data: dict):
        task = TaskRepository.get_by_id(task_id)
        if not task:
            return None
        
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
    def delete_task(task_id: int):
        task = TaskRepository.get_by_id(task_id)
        if not task:
            return False
        TaskRepository.delete(task)
        return True