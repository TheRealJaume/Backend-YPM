from pydantic import BaseModel, Field


class Task(BaseModel):
    task_name: str = Field(description="the task name")
    task_description: str = Field(description="the task description")


class Phase(BaseModel):
    name: str = Field(description="the phase name")
    tasks: list[Task] = Field(description="the list of the tasks corresponding to this phase")


# Define your desired data structure.
class DepartmentTask(BaseModel):
    department: str = Field(description="the department name")
    phases: list[Phase] = Field(description="the list of the phases")


class CompanyTask(BaseModel):
    name: str = Field(description="The company name")
    departments: list[DepartmentTask] = Field(description="The list of the departments")
