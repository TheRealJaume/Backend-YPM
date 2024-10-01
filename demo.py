from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_google_genai import GoogleGenerativeAI
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableParallel

from collections import defaultdict
from dotenv import load_dotenv

import re
import pandas as pd


class GeminiProjectManager:

    def __init__(self, company_name, company_definition, project_definition, project_tools, project_teams,
                 num_tasks_per_department, num_subtasks_per_department):

        self.company_name = company_name
        self.company_definition = company_definition
        self.project_definition = project_definition
        self.project_tools = project_tools
        self.project_teams = project_teams
        self.num_tasks_per_department = num_tasks_per_department
        self.num_subtasks_per_department = num_subtasks_per_department
        self.model = GoogleGenerativeAI(model="gemini-1.5-flash")

        # Diccionario para almacenar las tareas organizadas por departamento y fase
        self.tasks_dict = defaultdict(lambda: {"department": "", "phases": []})

    def generate_tasks(self):
        tasks = []

        load_dotenv()

        # Create a Gemini model
        model = GoogleGenerativeAI(model="gemini-1.5-flash")

        # Create a prompt template
        prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system",
                 "Eres un experto en gestión de proyectos. La empresa para la que estás trabajando es {company_name}."
                 "{company_definition}"
                 "El proyecto en el que estarás trabajando es {project_definition}."
                 "Las tecnologías utilizadas en el proyecto son {project_tools}."
                 "Los equipos del proyecto son {project_teams}."
                 "La respuesta debe estar en un formato de texto, evita los objetos json"
                 "Cada departamento debe venir precedido de ## y seguido de : (Ejm: ## Gestión:)"
                 "La respuesta no debe incluir ningún otro texto que el solicitado en la petición, eliminar explicaciones,"
                 "textos introductorios o definiciones de la respuesta"
                 ),
                ("user",
                 "Comencemos elaborando una lista de {num_tasks_per_department} tareas principales para cada uno de los equipos del proyecto, teniendo "
                 "en cuenta cada una de las fases del proyecto: "
                 "1. Planificación y toma de requisitos"
                 "2. Desarrollo e implementación"
                 "3. Entrega y puesta en producción"
                 ),
            ]
        )

        department_branch_chain = lambda department: (
                RunnableLambda(lambda x: self.divide_task_by_department(department, x))
                | RunnableLambda(lambda x: self.get_department_subtasks(x))
                | RunnableLambda(lambda x: self.get_department_task_estimation(x, department))
                | model
                | StrOutputParser()
        )

        departments = [dept.strip().lower() for dept in self.project_teams.split(",")]

        # Generar dinámicamente las ramas para el paralelismo de departamentos
        branches_phase_1 = {department: department_branch_chain(department) for department in departments}

        # Cadena de peticiones y estructuración de datos para obtener el resultado deseado
        chain = (
                prompt_template
                | model
                | StrOutputParser()
                | RunnableParallel(branches=branches_phase_1)
                # | RunnableLambda(lambda x: self.export_tasks_to_excel(x))
        )

        result = chain.invoke(
            {
                "company_name": self.company_name,
                "company_definition": self.company_definition,
                "project_definition": self.project_definition,
                "project_tools": self.project_tools,
                "project_teams": self.project_teams,
                "num_tasks_per_department": self.num_tasks_per_department
            }
        )
        print("TASK_DICT", self.tasks_dict)
        print(result)
        return tasks

    def divide_task_by_department(self, department, result):
        # Unir el resultado en un solo string
        result_str = ''.join(result)

        # Patrones para identificar fases y departamentos
        department_pattern = re.compile(r'## (\w+):')
        phase_pattern = re.compile(r'(\d+\.\s[^\n]+:)')

        # Dividir el resultado en secciones de departamentos
        department_sections = department_pattern.split(result_str)

        # Iterar sobre cada departamento identificado
        for i in range(1, len(department_sections), 2):
            current_department = department_sections[i].strip()

            # Si el departamento actual no coincide con el departamento buscado, saltar
            if current_department.lower() not in department.lower():
                continue

            # Obtener el contenido correspondiente a este departamento
            department_content = department_sections[i + 1]

            # Dividir el contenido por fases
            phase_sections = phase_pattern.split(department_content)

            # Iterar sobre las secciones de fase
            for j in range(1, len(phase_sections), 2):
                current_phase = phase_sections[j].strip()
                phase_content = phase_sections[j + 1]

                # Extraer tareas (sin el texto adicional)
                tasks = [task.replace('*', '').replace('- ', '').strip() for task in phase_content.split('\n') if
                         task.strip()]

                # Formatear las tareas con un contador manual para evitar que los índices sumen si no existe una tarea
                formatted_tasks = []
                task_counter = 1
                for task in tasks:
                    if task:  # Solo agregar si la tarea no está vacía
                        formatted_tasks.append({str(task_counter): task})
                        task_counter += 1

                # Solo añadir la fase si hay tareas no vacías
                if formatted_tasks:
                    # Agregar fase y tareas al diccionario del departamento correspondiente
                    if current_department not in self.tasks_dict:
                        self.tasks_dict[current_department] = {
                            "department": current_department,
                            "phases": []
                        }

                    self.tasks_dict[current_department]["phases"].append({
                        "phase": current_phase,
                        "tasks": formatted_tasks
                    })

        # Convertir a un diccionario normal (en lugar de defaultdict)
        return dict(self.tasks_dict)  # Retorna el diccionario si es necesario


    def get_department_subtasks(self, tasks_list):
        # Iterar sobre cada departamento en tasks_list
        for department, department_info in tasks_list.items():
            phases = department_info["phases"]

            # Iterar sobre cada fase dentro del departamento
            for phase in phases:
                tasks = phase["tasks"]

                # Iterar sobre cada tarea dentro de la fase
                for task in tasks:
                    # Acceder a la llave y valor de la tarea sin conocer la llave
                    task_key, task_value = list(task.items())[0]

                    # Crear un prompt para cada tarea
                    subtask_prompt = ChatPromptTemplate.from_messages(
                        [
                            ("system",
                             "Eres un experto en {department} y tienes que desarrollar {num_subtasks} subtareas para cada una de las tareas que se envían. "
                             "La respuesta debe estar en un formato de texto, evita los objetos json. "
                             "La respuesta no debe incluir ningún otro texto que el solicitado en la petición. "
                             "La respuesta debe tener el siguiente formato: -Subtarea 1: ..., -Subtarea 2: ..., etc."),
                            ("user",
                             "Crea la lista de las subtareas para la tarea enviada, teniendo en cuenta todos los aspectos necesarios para entregar de manera correcta y en tiempo "
                             "el proyecto que se está desarrollando. Esta es la tarea que tiene el departamento: {prompt_task}")
                        ]
                    )

                    # Crear una secuencia para invocar el modelo y parsear la salida
                    subtask_chain = (
                            subtask_prompt
                            | self.model
                            | StrOutputParser()
                    )

                    # Invocar el modelo pasando el prompt formateado como input
                    result = subtask_chain.invoke(
                        {"department": department,
                         "prompt_task": task_value,
                         "num_subtasks": self.num_subtasks_per_department
                         }
                    )

                    # Limpiar las subtareas generadas (en este caso, separadas por "- Subtarea X:")
                    subtasks = [line.replace("- ", "").strip() for line in result.split("\n") if line.strip()]

                    # Formatear las subtareas como un diccionario
                    formatted_subtasks = [{str(index + 1): subtask} for index, subtask in enumerate(subtasks)]

                    # Añadir las subtareas a la tarea actual en el diccionario
                    task["subtasks"] = formatted_subtasks
        return self.tasks_dict


ai_projectmanager = GeminiProjectManager(company_name="Google",
                                         company_definition="Nuestra empresa tecnológica de consultoría se especializa en ofrecer asesoramiento y soluciones en el ámbito de la tecnología de la información y la transformación digital. Ayudamos a organizaciones a optimizar sus procesos, implementar nuevas tecnologías y mejorar su infraestructura tecnológica para alcanzar sus objetivos estratégicos",
                                         project_definition="Diseñar una interfaz web intuitiva y atractiva para una compañía cervecera, que permita a los usuarios visualizar un listado detallado de surtidores. La interfaz mostrará información clave sobre cada surtidor, incluyendo su capacidad total y su estado actual (ya sea lleno o vacío), lo que facilitará la gestión y monitoreo de los recursos disponibles. Además, se incorporarán funcionalidades interactivas que permitirán a los usuarios filtrar y ordenar la información según sus necesidades, mejorando la experiencia de usuario y optimizando la toma de decisiones. La interfaz se desarrollará con un enfoque en la usabilidad y el diseño responsivo, asegurando que sea accesible desde dispositivos móviles y de escritorio, lo que permitirá a los empleados de la compañía cervecera realizar un seguimiento eficiente de los surtidores en cualquier momento y lugar.",
                                         project_tools="Frontend: React, Backend: Django",
                                         project_teams="Gestión, Desarrollo",
                                         num_tasks_per_department=1,
                                         num_subtasks_per_department=1)
ai_projectmanager.generate_tasks()
