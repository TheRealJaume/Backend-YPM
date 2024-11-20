from celery import shared_task, current_task

from project.projects.models import Project, ProjectRequirement
from project.projects.serializers import AITaskProjectSerializer, ProjectRequirementSerializer
from project.projects.utils import save_requirements_in_database
from project.sprints.serializers import AITaskOrganizationSerializer
from project.task.models import ProjectTask
from project.task.serializers import AITaskEstimationSerializer, AITaskAssignmentSerializer
from project.task.utils import serialize_project_tasks, save_tasks_in_database, save_assignment_in_database, \
    save_estimation_in_database, save_organization_in_database, serialize_sprint_tasks
from project.workers.models import ProjectWorker
from project.workers.serializers import AIProjectWorkerSerializer
from ypm_ai.tasks.managers.assign_tasks import TaskAssignmentManager
from ypm_ai.tasks.managers.create_tasks import ProjectTaskManager
from ypm_ai.tasks.managers.estimate_tasks import TaskEstimationManager
from ypm_ai.tasks.managers.organize_tasks import TaskOrganizationManager
from ypm_ai.tasks.managers.project_requirements import RequirementsManager


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
        saved, message = save_tasks_in_database(task_dict, project.id)
        result = serialize_project_tasks(project)
    except Exception as e:
        print("Error en la solicitud a AI-YPM:", e)
    return result


@shared_task
def request_assign_project_tasks(request_project):
    try:
        project = Project.objects.get(id=request_project)
        # Project tasks to be sent
        project_tasks = ProjectTask.objects.filter(project=project)
        many = True if project_tasks.count() > 1 else False
        project_tasks_data = project_tasks if project_tasks.count() > 1 else project_tasks.first()
        tasks = AITaskAssignmentSerializer(project_tasks_data, many=many).data
        # Project workers to be sent
        project_workers = ProjectWorker.objects.filter(project=project)
        many = True if project_workers.count() > 1 else False
        project_workers_data = project_workers if project_workers.count() > 1 else project_workers.first()
        workers = AIProjectWorkerSerializer(project_workers_data, many=many).data
        manager = TaskAssignmentManager(project_tasks=tasks, project_workers=workers,
                                        excel_file=False)
        assigend_task_dict = manager.assign_project_tasks()
        saved, message = save_assignment_in_database(assigend_task_dict)
        result = serialize_project_tasks(project)
    except Exception as e:
        print("Error en la solicitud a AI-YPM:", e)
    return result


@shared_task
def request_estimate_project_tasks(request_project):
    try:
        project = Project.objects.get(id=request_project)
        project_tasks = ProjectTask.objects.filter(project=project)
        many = True if project_tasks.count() > 1 else False
        project_tasks_data = project_tasks if project_tasks.count() > 1 else project_tasks.first()
        data = AITaskEstimationSerializer(project_tasks_data, many=many).data
        manager = TaskEstimationManager(project_tasks=data,
                                        excel_file=False)
        estimated_tasks = manager.estimate_project_tasks()
        saved, message = save_estimation_in_database(estimated_tasks)
        result = serialize_project_tasks(project)
    except Exception as e:
        print("Error en la solicitud a AI-YPM:", e)
    return result


@shared_task
def get_requirements_from_audio(file_path, project):
    try:
        # Paso 1: Transcribir el audio
        current_task.update_state(state="PROGRESS", meta={"progress": 20, "message": "Transcribing audio ..."})
        transcription = RequirementsManager().transcript_audio(file_path)
        manager = RequirementsManager(requirements_text=transcription)
        # Paso 2: Generar la transcripción
        current_task.update_state(state="PROGRESS", meta={"progress": 50, "message": "Generating requirements ..."})
        requirements = manager.get_requirements_from_conversation()
        project = Project.objects.get(id=project)
        # Paso 3: Guardando en bbdd
        current_task.update_state(state="PROGRESS", meta={"progress": 70, "message": "Saving in database ..."})
        saved, message = save_requirements_in_database(requirements=requirements, project=project)
        if saved:
            current_task.update_state(state="PROGRESS",
                                      meta={"progress": 100, "message": "Task completed", "file_path": file_path})
            project_requirements = ProjectRequirement.objects.filter(project=project)
            many = True if project_requirements.count() > 1 else False
            data = project_requirements if project_requirements.count() > 1 else project_requirements.first()
            serialized_requirements = ProjectRequirementSerializer(data, many=many)
            current_task.update_state(state="SUCCESS", meta={"progress": 100, "message": "Task completed",
                                                             "data": serialized_requirements.data,
                                                             "file_path": file_path})
        else:
            current_task.update_state(state="FAILURE",
                                      meta={"error": "Failed to save requirements", "file_path": file_path})
    except Exception as e:
        current_task.update_state(state="FAILURE",
                                  meta={"error": "Failed to process requirements", "file_path": file_path})
        print("Error en la solicitud a AI-YPM:", e)


@shared_task
def request_organize_project_tasks(request_project):
    try:
        project = Project.objects.get(id=request_project)
        project_tasks = ProjectTask.objects.filter(project=project)
        many = True if project_tasks.count() > 1 else False
        project_tasks_data = project_tasks if project_tasks.count() > 1 else project_tasks.first()
        data = AITaskOrganizationSerializer(project_tasks_data, many=many).data
        manager = TaskOrganizationManager(project_tasks=data,
                                          excel_file=False)
        estimated_tasks = manager.organize_project_tasks()
        saved, message = save_organization_in_database(estimated_tasks, project)
        result = serialize_sprint_tasks(project)
    except Exception as e:
        print("Error en la solicitud a AI-YPM:", e)
    return result
