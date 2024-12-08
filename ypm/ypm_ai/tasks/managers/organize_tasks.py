from dotenv import load_dotenv
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAI

from ypm_ai.tasks.prompts.sprint.models import NoSprints, ExistingSprints
from ypm_ai.tasks.prompts.sprint.text import task_organization_prompt


class TaskOrganizationManager:

    def __init__(self, project_tasks, sprints, excel_file):
        load_dotenv()
        self.project_tasks = project_tasks
        self.sprints = sprints
        self.model = GoogleGenerativeAI(model="gemini-1.5-flash")
        self.excel_file = excel_file

    def organize_project_tasks(self):
        # Create the department chain to create tasks for the project
        result = self.request_task_organization()
        return result

    def request_task_organization(self):
        # Request the tasks organized by sprints
        task_prompt = task_organization_prompt(tasks_list=self.project_tasks, sprints=self.sprints)

        # Set up a parser + inject instructions into the prompt template.
        parser = JsonOutputParser(pydantic_object=NoSprints if self.sprints is None else ExistingSprints)

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
