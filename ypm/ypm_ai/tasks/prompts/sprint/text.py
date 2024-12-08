# SPRINT
def task_organization_prompt(tasks_list, sprints):
    prompt_1 = "Eres un experto en gestión de proyectos, para ello tomarás la información necesaria de todas tus fuentes" \
               "de información para organizar las tareas que te envío a continuación en diferentes sprints." \
               "Ten en cuenta la prioridad de cada una de las tareas, así como el tiempo que se va a invertir en realizarlas" \
               "A continuación, te envío la lista de tareas que deberás organizar"
    prompt_no_sprints = "en sprints, el resultado deberá de ser una lista de sprints, con la estimación de tiempo necesario " \
                        "para cada uno de ellos, el objetivo a cumplir en el sprint" \
                        " y el listado de las tareas que están incluidas en ese sprint."
    prompt_sprints = "en los siguientes sprints existentes: {sprints}."
    prompt_3 = " Cada una de las tareas tiene los siguientes campos:" \
               "Id: valor identificativo de la tarea" \
               "Name:Nombre de la tarea" \
               "Description: descripción detallada del objetivo a realizar con la tarea" \
               "time: Tiempo estimado en horas necesarias para poder completar la tarea" \
               "worker: Trabajador responsable de realizar la tarea" \
               "Esta es la lista de tareas: {requirements_text}"

    # Condicional para elegir el prompt correcto
    if sprints:
        full_prompt = prompt_1 + prompt_sprints + prompt_3
        full_prompt = full_prompt.format(requirements_text=tasks_list, sprints=sprints)
    else:
        full_prompt = prompt_1 + prompt_no_sprints + prompt_3
        full_prompt = full_prompt.format(requirements_text=tasks_list)
    return full_prompt
