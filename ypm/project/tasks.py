from celery import shared_task

from project.projects.models import Project
from project.projects.serializers import AITaskProjectSerializer
from project.task.utils import serialize_project_tasks, save_tasks_in_database
from ypm_ai.tasks.managers.create_tasks import ProjectTaskManager


@shared_task
def request_project_tasks(request_project):
    try:
        project = Project.objects.get(id=request_project)
        data = AITaskProjectSerializer(project).data
        manager = ProjectTaskManager(company_name=data['company']['name'],
                                     company_definition=data['company']['description'],
                                     project_definition=data['description'],
                                     project_technologies=", ".join(
                                         [item['name'] for item in data['technologies']]),
                                     project_departments=", ".join(
                                         [item['name'] for item in data['departments']]),
                                     project_requirements=data['requirements'],
                                     num_tasks_per_department=1,
                                     num_tasks_per_phase=1,
                                     num_subtasks_per_department=1,
                                     excel_file=False)
        task_dict = manager.generate_project_tasks()
        project = Project.objects.get(id=project.id)
        saved, message = save_tasks_in_database(task_dict, project.id)
        result = serialize_project_tasks(project)
    except Exception as e:
        print("Error en la solicitud a AI-YPM:", e)
    return result
