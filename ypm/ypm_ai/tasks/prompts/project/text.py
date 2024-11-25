def project_task_prompt(company_name, company_definition, project_definition, project_technologies, project_departments,
                        project_requirements, num_tasks_per_department):
    prompt_1 = "Eres un experto en gestión de proyectos. Asumiendo el rol de gestor de proyectos en {company_name}," \
               "una empresa dedicada a {company_definition}, desarrollarás un plan detrabajo detallado para el " \
               "proyecto {project_definition}.Este proyecto involucra lastecnologías {project_technologies} y cuenta " \
               "con la participación de los equipos {project_departments}. Tu objetivo consiste en generar una tarea " \
               "para cada una de las siguientes fases del proyecto:1. Planificación y toma de requisitos 2. Desarrollo e " \
               "implementación 3. Entrega y puesta en producción. Proporciona una lista de tareas {num_tasks_per_department} para cada fase del " \
               "proyecto y departamentos, teniendo en cuenta los requerimientos que te presento a " \
               "continuación: {project_requirements}. "
    prompt_1 = prompt_1.format(company_name=company_name, company_definition=company_definition,
                               project_definition=project_definition, project_technologies=project_technologies,
                               project_departments=project_departments, project_requirements=project_requirements,
                               num_tasks_per_department=num_tasks_per_department)
    return prompt_1


def department_task_prompt():
    prompt_1 = "Eres un experto en gestión de proyectos. Asumiendo el rol de equipo en {department},"
    return prompt_1


def department_phase_prompt():
    prompt_1 = "Eres un experto en gestión de proyectos. Asumiendo el rol de {department} en la fase {phase},"
    return prompt_1


# REQUIREMENTS
def summarize_requirements_prompt(requirements_text):
    prompt_1 = "Eres un experto en gestión de proyectos, para ello tomarás la información necesaria de todas tus fuentes" \
               "de información para determinar cuales son los puntos clave a tener el cuenta para el correcto desarrollo" \
               "del proyecto. Este proyecto viene definido a partir de una reunión entre el cliente y la empresa que lo" \
               "desarrolla. A continuación, te envío un texto de esta reunión donde vienen identificados cada uno de los" \
               "presentes en la conversación. El resultado debe ser una lista de requerimientos basados en la conversacion" \
               "que te voy a enviar. {requirements_text}"
    prompt_1 = prompt_1.format(requirements_text=requirements_text)
    return prompt_1


def get_requirements_from_text_prompt():
    prompt_1 = "Eres un experto en gestión de proyectos, para ello tomarás la información necesaria de todas tus fuentes" \
               "de información para determinar cuales son los puntos clave a tener el cuenta para el correcto desarrollo" \
               "del proyecto. Este proyecto viene definido a partir de una reunión entre el cliente y la empresa que lo" \
               "desarrolla. A continuación, te envío un documento que recoge los requisitos necesarios para realizar el " \
                "proyecto. El resultado debe ser una lista de requerimientos basados en el documento de texto enviado y" \
               "los requerimientos tienen que venir en español como el documento."
    prompt_1 = prompt_1.format()
    return prompt_1