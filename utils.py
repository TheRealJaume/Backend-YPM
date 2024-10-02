


def export_tasks_to_excel(self, chain_output, filename='project_tasks.xlsx'):
        # Crear una lista vacía para almacenar los datos
        data = []

        # Iterar sobre cada departamento en el output
        for department, tasks in chain_output['branches'].items():
            # Dividir el string en tareas
            tasks_sections = re.split(r'\*\*Tarea \d+:', tasks)  # Separar por tareas

            # Iterar sobre las secciones de tareas
            for task_section in tasks_sections[1:]:  # Ignorar la primera sección vacía
                task_lines = task_section.split('\n')  # Dividir por líneas

                # Tomar el nombre de la tarea
                task_name = task_lines[0].strip() if task_lines else "Tarea desconocida"

                # Iterar sobre las líneas de subtareas
                for line in task_lines[1:]:
                    line = line.strip()
                    if line:  # Asegurarse de que la línea no esté vacía
                        # Buscar subtarea y tiempo utilizando regex
                        match = re.match(r'^\* (Subtarea [\d.]+:.*?)(\s*\((\d+h)\))?', line)
                        if match:
                            subtask_name = match.group(1).strip()
                            time_estimate = match.group(3) if match.group(3) else 'No especificado'

                            # Añadir a la lista de datos
                            data.append({
                                'Departamento': department,
                                'Tarea': task_name,
                                'Subtarea': subtask_name,
                                'Estimación de Tiempo': time_estimate
                            })

        # Crear un DataFrame de pandas
        df = pd.DataFrame(data)

        # Guardar el DataFrame en un archivo Excel
        df.to_excel(filename, index=False, engine='openpyxl')

        print(f"Las tareas han sido exportadas a '{filename}' exitosamente.")
