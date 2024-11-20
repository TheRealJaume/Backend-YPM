from pydantic import BaseModel, Field


class Task(BaseModel):
    task_id: str = Field(description="the task id sent in the prompt")


class Sprint(BaseModel):
    name: str = Field(description="the phase name")
    time: int = Field(description="the time needed to complete all the tasks in the sprint. This value is defined by "
                                  "adding the estimation of the time needed to complete every task of the sprint. Value"
                                  "must be expressed on days")
    target: str = Field(description="The target to be completed when the sprint is finished by completing the tasks")
    tasks: list[Task] = Field(description="the list of tasks to be completed when the sprint is finished")


class Sprints(BaseModel):
    sprint: list[Sprint] = Field(
        description="the organization where some tasks are included to be done in a defined time")
