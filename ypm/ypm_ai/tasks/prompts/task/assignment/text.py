def task_assignment_prompt(project_tasks, project_workers):
    prompt_1 = "Realiza una asignación de tareas a cada trabajador teniendo en cuenta la dificultad de las tareas y el nivel" \
               "de cada uno de los trabajadores. A continuación, recibirás una lista de tareas (nombre, descripción) " \
               "y una lista de trabajadores con sus características (id, level, technologies ) " \
               "Lista de trabajadores: {project_workers}." \
               "Lista de tareas: {project_tasks}."
    prompt_1 = prompt_1.format(project_tasks=project_tasks, project_workers=project_workers)
    return prompt_1
