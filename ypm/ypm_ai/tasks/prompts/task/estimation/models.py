from pydantic import BaseModel, Field


class EstimatedTask(BaseModel):
    id: str = Field(description="the id of the task sent to the server")
    task_name: str = Field(description="the task name")
    task_description: str = Field(description="the task description")
    task_estimation: int = Field(description="the time estimated in hours for the task")


class EstimatedTasks(BaseModel):
    estimated_tasks: list[EstimatedTask] = Field(description="the list of the estimated tasks")
