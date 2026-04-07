from db.database import tasks_collection

class TaskAgent:

    def execute(self, task: str):
        task_data = {
            "task": task,
            "status": "created"
        }

        tasks_collection.insert_one(task_data)

        return {
            "status": "task_created",
            "details": f"Task stored in DB: {task}"
        }