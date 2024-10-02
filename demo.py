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
                 num_tasks_per_department, num_subtasks_per_department, excel_file):

        load_dotenv()

        self.company_name = company_name
        self.company_definition = company_definition
        self.project_definition = project_definition
        self.project_tools = project_tools
        self.project_teams = project_teams
        self.num_tasks_per_department = num_tasks_per_department
        self.num_subtasks_per_department = num_subtasks_per_department
        self.model = GoogleGenerativeAI(model="gemini-1.5-flash")
        self.excel_file = excel_file

        # Diccionario para almacenar las tareas organizadas por departamento y fase
        self.tasks_dict = defaultdict(lambda: {"department": "", "phases": []})

    def generate_tasks(self):

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
                # | RunnableLambda(lambda x: self.get_department_subtasks(x))
                | RunnableLambda(lambda x: self.get_department_task_estimation(x, department))
        )

        departments = [dept.strip() for dept in self.project_teams.split(",")]

        # Generar dinámicamente las ramas para el paralelismo de departamentos
        branches_phase_1 = {department: department_branch_chain(department) for department in departments}

        # Cadena de peticiones y estructuración de datos para obtener el resultado deseado
        chain = (
                prompt_template
                | model
                | StrOutputParser()
                | RunnableParallel(branches=branches_phase_1)
        )

        if self.excel_file:
            self.export_tasks_to_excel()

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
        return result

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
                        formatted_tasks.append({str(task_counter): {'description': task}})
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

    def get_department_task_estimation(self, task_dict, department):
        # Filtrar el input para el departamento
        task_list = task_dict[department]['phases']

        # Crear un prompt específicamente para subtareas del departamento
        estimation_prompt = ChatPromptTemplate.from_messages(
            [
                ("system",
                 "Eres un experto en estimaciones de tiempos y tienes que definir el tiempo que se invierte en cada una de las tareas y subtareas que se envían."
                 " La respuesta debe estar en un formato de texto, evita los objetos json."
                 " La respuesta no debe incluir ningún otro texto que el solicitado en la petición."
                 " La respuesta debe ser el mismo diccionario que se envía con las horas incluidas como un elemento más en cada tarea con la llave hours."),
                ("user",
                 "Incluye entre paréntesis (EJM. 1. Definicion de tarea (8)) la estimación de cada una de las fases, tareas y subtareas que aparecen a continuación:"
                 "{task_list}")
            ]
        )

        # Crear una secuencia para invocar el modelo y parsear la salida
        estimation_chain = (
                estimation_prompt
                | self.model
                | StrOutputParser()
        )

        # Invocar el modelo pasando el prompt formateado como input
        result = estimation_chain.invoke(
            {"task_list": task_list}
        )
        # Procesar el resultado para añadir estimaciones al diccionario
        estimated_tasks = result.split('\n')

        # Actualizar el diccionario
        self.tasks_dict[department] = estimated_tasks

    def list_tasks_from_phases(self, task_list):
        # Crear una lista única para todas las tareas
        listed_tasks = []

        # Recorrer cada fase y agregar las tareas a la lista all_tasks
        for phase in task_list:
            for task in phase['tasks']:
                # Acceder al valor de la tarea, independientemente de la clave (que es un número como string)
                task_description = list(task.values())[0]
                listed_tasks.append(task_description)
        return listed_tasks

    def export_tasks_to_excel(self, filename="tasks.xlsx"):
        # Crear una lista vacía para almacenar los datos
        data = []

        # Iterar sobre cada departamento en el diccionario TASK_DICT
        for department, tasks in self.tasks_dict.items():
            # Convertir el string de tareas a una lista de diccionarios usando eval (con precaución)
            try:
                phases = eval(tasks[0])  # El primer elemento de la lista es el contenido real de las fases y tareas
            except Exception as e:
                print(f"Error al evaluar las tareas del departamento {department}: {e}")
                continue

            # Iterar sobre las fases
            for phase in phases:
                phase_name = phase['phase']

                # Iterar sobre las tareas dentro de cada fase
                for task in phase['tasks']:
                    for task_id, task_details in task.items():
                        task_description = task_details['description']
                        time_estimate = task_details.get('horas', task_details.get('hours', 'No especificado'))

                        # Añadir a la lista de datos
                        data.append({
                            'Departamento': department,
                            'Fase': phase_name,
                            'Tarea': f"Tarea {task_id}",
                            'Descripción de la Tarea': task_description,
                            'Estimación de Tiempo': time_estimate
                        })

        # Crear un DataFrame de pandas
        df = pd.DataFrame(data)

        # Guardar el DataFrame en un archivo Excel
        df.to_excel(filename, index=False, engine='openpyxl')

        print(f"Las tareas han sido exportadas a '{filename}' exitosamente.")


ai_projectmanager = GeminiProjectManager(company_name="Google",
                                         company_definition="Nuestra empresa tecnológica de consultoría se especializa en ofrecer asesoramiento y soluciones en el ámbito de la tecnología de la información y la transformación digital. Ayudamos a organizaciones a optimizar sus procesos, implementar nuevas tecnologías y mejorar su infraestructura tecnológica para alcanzar sus objetivos estratégicos",
                                         project_definition="Diseñar una interfaz web intuitiva y atractiva para una compañía cervecera, que permita a los usuarios visualizar un listado detallado de surtidores. La interfaz mostrará información clave sobre cada surtidor, incluyendo su capacidad total y su estado actual (ya sea lleno o vacío), lo que facilitará la gestión y monitoreo de los recursos disponibles. Además, se incorporarán funcionalidades interactivas que permitirán a los usuarios filtrar y ordenar la información según sus necesidades, mejorando la experiencia de usuario y optimizando la toma de decisiones. La interfaz se desarrollará con un enfoque en la usabilidad y el diseño responsivo, asegurando que sea accesible desde dispositivos móviles y de escritorio, lo que permitirá a los empleados de la compañía cervecera realizar un seguimiento eficiente de los surtidores en cualquier momento y lugar.",
                                         project_tools="Frontend: React, Backend: Django",
                                         project_teams="Gestión, Desarrollo",
                                         num_tasks_per_department=1,
                                         num_subtasks_per_department=1,
                                         excel_file=False)
ai_projectmanager.generate_tasks()
