def task_estimation_prompt(project_tasks):
    prompt_1 = "Estima el tiempo necesario (horas) para realizar cada una de las tareas que se envían a continuación. Las " \
               "tareas vienen estructuradas en una lista donde los diferentes elementos son las diferentes tareas que " \
               "hay que estimar. Cada tarea viene en un diccionario con la siguiente estructura: " \
               "'id': (Número identificador de la tarea),'name': (Nombre de la tarea), 'description': (Descripción de la tarea)" \
               "Proporciona una estimación real en horas de cada una de las tareas enviadas. Las tareas son {project_tasks}"
    prompt_1 = prompt_1.format(project_tasks=project_tasks)
    return prompt_1
