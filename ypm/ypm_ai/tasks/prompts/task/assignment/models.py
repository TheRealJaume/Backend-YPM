from pydantic import BaseModel, Field


class AssignedTask(BaseModel):
    id: str = Field(description="the id of the task sent to the server")
    worker_id: str = Field(description="the worker id assigned to the task")
    # TODO: Modificar para que se pueden asignar más de un trabajador a cada tarea


class AssignedTasks(BaseModel):
    asigned_tasks: list[AssignedTask] = Field(description="the list of the assigned tasks")
