def project_task_prompt(company_name, company_definition, project_definition, project_technologies, project_departments,
                        project_requirements):
    prompt_1 = "Eres un experto en gestión de proyectos. Asumiendo el rol de gestor de proyectos en {company_name}," \
               "una empresa dedicada a {company_definition}, desarrollarás un plan detrabajo detallado para el " \
               "proyecto {project_definition}.Este proyecto involucra lastecnologías {project_technologies} y cuenta " \
               "con la participación de los equipos {project_departments}. Tu objetivo consiste en generar una tarea " \
               "para cada una de las siguientes fases del proyecto:1. Planificación y toma de requisitos 2. Desarrollo e " \
               "implementación 3. Entrega y puesta en producción. Proporciona una tarea principal para cada fase del " \
               "proyecto y departamentos, teniendo en cuenta los requerimientos que te presento a " \
               "continuación: {project_requirements}. "
    prompt_1 = prompt_1.format(company_name=company_name, company_definition=company_definition,
                               project_definition=project_definition, project_technologies=project_technologies,
                               project_departments=project_departments, project_requirements=project_requirements)
    return prompt_1


def department_task_prompt():
    prompt_1 = "Eres un experto en gestión de proyectos. Asumiendo el rol de equipo en {department},"
    return prompt_1


def department_phase_prompt():
    prompt_1 = "Eres un experto en gestión de proyectos. Asumiendo el rol de {department} en la fase {phase},"
    return prompt_1
