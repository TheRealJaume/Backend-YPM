from dotenv import load_dotenv
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAI

from ypm_ai.tasks.prompts.project.models import CompanyTask
from ypm_ai.tasks.prompts.project.text import project_task_prompt


class ProjectTaskManager:

    def __init__(self, company_name, company_definition, project_definition, project_technologies, project_departments,
                 num_tasks_per_department, num_tasks_per_phase, num_subtasks_per_department,project_requirements,
                 excel_file):
        load_dotenv()
        self.company_name = company_name
        self.company_definition = company_definition
        self.project_definition = project_definition
        self.project_technologies = project_technologies
        self.project_departments = project_departments
        self.num_tasks_per_department = num_tasks_per_department
        self.num_tasks_per_phase = num_tasks_per_phase
        self.project_requirements = project_requirements
        self.num_subtasks_per_department = num_subtasks_per_department
        self.model = GoogleGenerativeAI(model="gemini-1.5-flash")
        self.excel_file = excel_file

    def generate_project_tasks(self):
        # Create the department chain to create tasks for the project
        result = self.request_task_per_department()
        return result

    def request_task_per_department(self):
        # Request the number of tasks per department and per phase
        task_prompt = project_task_prompt(company_name=self.company_name, company_definition=self.company_definition,
                                          project_definition=self.project_definition,
                                          project_technologies=self.project_technologies,
                                          project_departments=self.project_departments,
                                          project_requirements=self.project_requirements,
                                          num_tasks_per_department=self.num_tasks_per_department)

        # Set up a parser + inject instructions into the prompt template.
        parser = JsonOutputParser(pydantic_object=CompanyTask)

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