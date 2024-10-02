from managers import GeminiProjectManager

ai_projectmanager = GeminiProjectManager(company_name="Google",
                                         company_definition="Nuestra empresa tecnológica de consultoría se especializa en ofrecer asesoramiento y soluciones en el ámbito de la tecnología de la información y la transformación digital. Ayudamos a organizaciones a optimizar sus procesos, implementar nuevas tecnologías y mejorar su infraestructura tecnológica para alcanzar sus objetivos estratégicos",
                                         project_definition="Diseñar una interfaz web intuitiva y atractiva para una compañía cervecera, que permita a los usuarios visualizar un listado detallado de surtidores. La interfaz mostrará información clave sobre cada surtidor, incluyendo su capacidad total y su estado actual (ya sea lleno o vacío), lo que facilitará la gestión y monitoreo de los recursos disponibles. Además, se incorporarán funcionalidades interactivas que permitirán a los usuarios filtrar y ordenar la información según sus necesidades, mejorando la experiencia de usuario y optimizando la toma de decisiones. La interfaz se desarrollará con un enfoque en la usabilidad y el diseño responsivo, asegurando que sea accesible desde dispositivos móviles y de escritorio, lo que permitirá a los empleados de la compañía cervecera realizar un seguimiento eficiente de los surtidores en cualquier momento y lugar.",
                                         project_tools="Frontend: React, Backend: Django",
                                         project_teams="Gestión, Desarrollo",
                                         num_tasks_per_department=1,
                                         num_subtasks_per_department=1,
                                         excel_file=True)
ai_projectmanager.generate_tasks()
