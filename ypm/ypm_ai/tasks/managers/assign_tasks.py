from dotenv import load_dotenv
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAI

from ypm_ai.tasks.prompts.task.assignment.models import AssignedTasks
from ypm_ai.tasks.prompts.task.assignment.text import task_assignment_prompt


class TaskAssignmentManager:

    def __init__(self, project_tasks, project_workers, excel_file):
        load_dotenv()
        self.project_tasks = project_tasks
        self.project_workers = project_workers
        self.model = GoogleGenerativeAI(model="gemini-1.5-flash")
        self.excel_file = excel_file

    def assign_project_tasks(self):
        # Request the number of tasks per department and per phase
        task_prompt = task_assignment_prompt(self.project_tasks, self.project_workers)

        # Set up a parser + inject instructions into the prompt template.
        parser = JsonOutputParser(pydantic_object=AssignedTasks)

        prompt = PromptTemplate(
            template="Answer the user query.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        department_chain = (
                prompt
                | self.model
                | parser)

        result = department_chain.invoke({
            "query": task_prompt
        })
        return result