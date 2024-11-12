from dotenv import load_dotenv
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAI

from tasks.prompts.task.estimation.models import EstimatedTasks
from tasks.prompts.task.estimation.text import task_estimation_prompt


class TaskEstimationManager:

    def __init__(self, project_tasks, excel_file):
        load_dotenv()
        self.project_tasks = project_tasks
        self.model = GoogleGenerativeAI(model="gemini-1.5-flash")
        self.excel_file = excel_file

    def estimate_project_tasks(self):
        # Create the department chain to create tasks for the project
        result = self.request_task_estimation()
        return result

    def request_task_estimation(self):
        # Request the number of tasks per department and per phase
        task_prompt = task_estimation_prompt(project_tasks=self.project_tasks)

        # Set up a parser + inject instructions into the prompt template.
        parser = JsonOutputParser(pydantic_object=EstimatedTasks)

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
