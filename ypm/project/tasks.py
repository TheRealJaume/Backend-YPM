import os

from celery import shared_task, current_task
from django.conf import settings
from django.core.files.storage import default_storage
from django.utils.module_loading import import_string

from project.departments.models import ProjectDepartment
from project.projects.models import Project
from project.projects.serializers import AITaskProjectSerializer
from project.projects.utils import save_requirements_in_database, save_requirements_from_text_file
from project.requirements.models import ProjectRequirement
from project.requirements.serializers import ProjectRequirementSerializer
from project.sprints.models import ProjectSprint
from project.sprints.serializers import AITaskOrganizationSerializer, AITSprintOrganizationBasicSerializer
from project.task.models import ProjectTask
from project.task.serializers import AITaskEstimationSerializer, AITaskAssignmentSerializer
from project.task.utils import serialize_project_tasks, save_project_tasks_in_database, save_assignment_in_database, \
    save_estimation_in_database, save_organization_in_database, serialize_sprint_tasks, \
    save_department_tasks_in_database
from project.workers.models import ProjectWorker
from project.workers.serializers import AIProjectWorkerSerializer
from ypm.celery import get_storage
from ypm_ai.tasks.managers.assign_tasks import TaskAssignmentManager
from ypm_ai.tasks.managers.create_tasks import ProjectTaskManager
from ypm_ai.tasks.managers.estimate_tasks import TaskEstimationManager
from ypm_ai.tasks.managers.organize_tasks import TaskOrganizationManager
from ypm_ai.tasks.managers.project_requirements import RequirementsManager
import logging

logger = logging.getLogger(__name__)

@shared_task
def request_project_tasks(request_project):
    try:
        # Paso 0: Crear Manager
        current_task.update_state(state="PENDING", meta={"progress": 1,
                                                          "message": f"Creating project tasks..."
                                                          })
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
                                     num_tasks_per_department=10,
                                     num_tasks_per_phase=10,
                                     num_subtasks_per_department=10,
                                     excel_file=False)
        total_departments = len(data['departments'])
        for i, department in enumerate(data['departments'], start=1):
            # Paso 1: Crear tareas para el departamento (department)
            current_progress = ((i / total_departments) * 100) - 1
            current_task.update_state(state="PENDING",
                                      meta={"progress": current_progress if current_progress > 0 else 5,
                                            "message": f"Creating tasks for department {department['name']}"
                                            })
            task_dict = manager.request_task_per_department(department)
            # Paso 2: Guardar las tareas para el departamento (department)
            current_task.update_state(state="PENDING",
                                      meta={"progress": current_progress if current_progress > 0 else 5,
                                            "message": f"Saving tasks for department {department['name']}"
                                            })
            saved, message = save_department_tasks_in_database(task_dict, project)
        # Paso 3: Serializar las tareas para todos los departamentos
        result = serialize_project_tasks(project)
        current_task.update_state(state="SUCCESS", meta={"progress": 99, "message": "Tasks created successfully",
                                                         "data": result})
    except Exception as e:
        current_task.update_state(
            state="FAILURE",
            meta={
                "error": str(e),
                "exc_type": type(e).__name__
            }
        )


@shared_task
def request_assign_project_tasks(request_project):
    try:
        # Paso 0: Crear Manager
        current_task.update_state(state="PENDING", meta={"progress": 1,
                                                          "message": f"Assigning project tasks..."
                                                          })
        project = Project.objects.get(id=request_project)
        # Project tasks to be sent
        departments = ProjectDepartment.objects.filter(project=project)
        # Project workers to be sent
        project_workers = ProjectWorker.objects.filter(project=project)
        many = True if project_workers.count() > 1 else False
        project_workers_data = project_workers if project_workers.count() > 1 else project_workers.first()
        workers = AIProjectWorkerSerializer(project_workers_data, many=many).data
        # Iterate over all departments to get the tasks for each of them
        total_departments = departments.count()
        for i, department in enumerate(departments, start=1):
            # Paso 1: Asignar tareas para el departamento (department)
            current_progress = ((i / total_departments) * 100) - 1
            current_task.update_state(state="PENDING",
                                      meta={"progress": current_progress if current_progress > 0 else 5,
                                            "message": f"Assigning tasks to department {department.department.name}"
                                            })
            department_tasks = ProjectTask.objects.filter(department=department)
            many = True if department_tasks.count() > 1 else False
            project_tasks_data = department_tasks if department_tasks.count() > 1 else department_tasks.first()
            tasks = AITaskAssignmentSerializer(project_tasks_data, many=many).data
            manager = TaskAssignmentManager(project_tasks=tasks, project_workers=workers,
                                            excel_file=False)
            assigned_tasks = manager.assign_project_tasks()
            # Paso 2: Guardar las asignaciones para el departamento (department)
            current_task.update_state(state="PENDING",
                                      meta={"progress": current_progress if current_progress > 0 else 5,
                                            "message": f"Saving assignments for department {department.department.name}"
                                            })
            saved, message = save_assignment_in_database(assigned_tasks)
        result = serialize_project_tasks(project)
        current_task.update_state(state="SUCCESS", meta={"progress": 99, "message": "Assignments created successfully",
                                                         "data": result})
    except Exception as e:
        current_task.update_state(
            state="FAILURE",
            meta={
                "error": str(e),
                "exc_type": type(e).__name__
            }
        )


@shared_task
def request_estimate_project_tasks(request_project):
    try:
        # Paso 0: Crear Manager
        current_task.update_state(state="PENDING", meta={"progress": 1,
                                                          "message": f"Estimating project tasks..."
                                                          })
        project = Project.objects.get(id=request_project)
        project_tasks = ProjectTask.objects.filter(project=project)
        departments = ProjectDepartment.objects.filter(project=project)
        total_departments = departments.count()
        for i, department in enumerate(departments, start=1):
            # Paso 1: Asignar tareas para el departamento (department)
            current_progress = ((i / total_departments) * 100) - 1
            current_task.update_state(state="PENDING",
                                      meta={"progress": current_progress if current_progress > 0 else 5,
                                            "message": f"Estimating tasks of department {department.department.name}"
                                            })
            department_tasks = project_tasks.filter(department=department)
            many = True if department_tasks.count() > 1 else False
            department_tasks_data = department_tasks if department_tasks.count() > 1 else department_tasks.first()
            data = AITaskEstimationSerializer(department_tasks_data, many=many).data
            manager = TaskEstimationManager(project_tasks=data,
                                            excel_file=False)
            estimated_tasks = manager.estimate_project_tasks()
            # Paso 2: Guardar las asignaciones para el departamento (department)
            current_task.update_state(state="PENDING",
                                      meta={"progress": current_progress if current_progress > 0 else 5,
                                            "message": f"Saving estimations of department {department.department.name}"
                                            })
            saved, message = save_estimation_in_database(estimated_tasks)
        result = serialize_project_tasks(project)
        current_task.update_state(state="SUCCESS", meta={"progress": 99, "message": "Estimation successfully created",
                                                         "data": result})
    except Exception as e:
        current_task.update_state(
            state="FAILURE",
            meta={
                "error": str(e),
                "exc_type": type(e).__name__
            }
        )


@shared_task
def request_organize_project_tasks(request_project):
    try:
        # Paso 0: Crear Manager
        current_task.update_state(state="PENDING", meta={"progress": 1,
                                                          "message": f"Organizing project tasks..."
                                                          })
        # Get the project tasks
        project = Project.objects.get(id=request_project)
        project_tasks = ProjectTask.objects.filter(project=project)
        # Get the departments for the project
        departments = ProjectDepartment.objects.filter(project=project)
        # Iterate through the departments to organize tasks
        total_departments = departments.count()
        for i, department in enumerate(departments, start=1):
            current_progress = ((i / total_departments) * 100) - 1
            current_task.update_state(state="PENDING",
                                      meta={"progress": current_progress if current_progress > 0 else 5,
                                            "message": f"Organizing tasks of department {department.department.name}"
                                            })
            # Get the department tasks
            department_tasks = project_tasks.filter(department=department)
            many = True if department_tasks.count() > 1 else False
            department_tasks_data = department_tasks if department_tasks.count() > 1 else department_tasks.first()
            data = AITaskOrganizationSerializer(department_tasks_data, many=many).data
            # Look for existing sprints
            project_sprints = project_tasks.filter(sprint__isnull=False).values_list('sprint', flat=True)
            if project_sprints.count() > 0:
                project_sprints_objects = ProjectSprint.objects.filter(id__in=project_sprints)
                many = True if project_sprints_objects.count() > 1 else False
                project_sprints_data = project_sprints_objects if project_sprints_objects.count() > 1 else project_sprints_objects.first()
                sprints_data = AITSprintOrganizationBasicSerializer(project_sprints_data, many=many).data
            else:
                sprints_data = None
            manager = TaskOrganizationManager(project_tasks=data,
                                              sprints=sprints_data,
                                              excel_file=False)
            estimated_tasks = manager.organize_project_tasks()
            # Paso 2: Guardar las asignaciones para el departamento (department)
            current_task.update_state(state="PENDING",
                                      meta={"progress": current_progress if current_progress > 0 else 5,
                                            "message": f"Saving organization of department {department.department.name}"
                                            })
            saved, message = save_organization_in_database(estimated_tasks, project)
        result = serialize_sprint_tasks(project)
        current_task.update_state(state="SUCCESS",
                                  meta={"progress": 99, "message": "Organization successfully created",
                                        "data": result})
    except Exception as e:
        current_task.update_state(
            state="FAILURE",
            meta={
                "error": str(e),
                "exc_type": type(e).__name__
            }
        )


@shared_task
def get_requirements_from_audio(file_path, project):
    try:
        # Paso 1: Transcribir el audio
        current_task.update_state(state="PENDING", meta={"progress": 20, "message": "Transcribing audio ..."})
        # Usa la URL del archivo si es almacenamiento S3
        storage_instance = get_storage()
        is_s3_storage = "storages" in storage_instance.__class__.__module__
        file_url = default_storage.url(file_path) if is_s3_storage else os.path.join(settings.MEDIA_ROOT, file_path)
        transcription = RequirementsManager().transcript_audio(file_url)
        manager = RequirementsManager(requirements_text=transcription)
        # Paso 2: Generar la transcripción
        current_task.update_state(state="PENDING", meta={"progress": 50, "message": "Generating requirements ..."})
        requirements = manager.get_requirements_from_conversation()
        project = Project.objects.get(id=project)
        # Paso 3: Guardando en bbdd
        current_task.update_state(state="PENDING", meta={"progress": 70, "message": "Saving in database ..."})
        saved, message = save_requirements_in_database(requirements=requirements, project=project)
        if saved:
            current_task.update_state(state="PENDING",
                                      meta={"progress": 99, "message": "Task completed", "file_path": file_path})
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
        current_task.update_state(
            state="FAILURE",
            meta={
                "error": str(e),
                "exc_type": type(e).__name__,
                "file_path": file_path,
            }
        )


def get_storage():
    """Carga la clase de almacenamiento predeterminada configurada en Django settings."""
    StorageClass = import_string(settings.DEFAULT_FILE_STORAGE)
    return StorageClass()

@shared_task
def get_requirements_from_text(file_path, project):
    try:
        current_task.update_state(state="PENDING", meta={"progress": 20, "message": "Uploading document..."})
        # Usa la URL del archivo si es almacenamiento S3
        storage_instance = get_storage()
        is_s3_storage = "storages" in storage_instance.__class__.__module__
        file_url = default_storage.url(file_path) if is_s3_storage else os.path.join(settings.MEDIA_ROOT, file_path)
        text_manager = RequirementsManager(text_file=file_url)
        current_task.update_state(state="PENDING", meta={"progress": 40, "message": "Extracting requirements..."})
        requirements = text_manager.get_requirements_from_text()
        current_task.update_state(state="PENDING", meta={"progress": 60, "message": "Summarizing requirements..."})
        project = Project.objects.get(id=project)
        # Paso 2: Guardando en bbdd
        current_task.update_state(state="PENDING",
                                  meta={"progress": 70, "message": "Saving requirements in database ..."})
        saved, message = save_requirements_from_text_file(requirements=requirements, project=project)
        if saved:
            project_requirements = ProjectRequirement.objects.filter(project=project)
            many = True if project_requirements.count() > 1 else False
            data = project_requirements if project_requirements.count() > 1 else project_requirements.first()
            serialized_requirements = ProjectRequirementSerializer(data, many=many)
            current_task.update_state(state="SUCCESS", meta={"progress": 99, "message": "Task completed",
                                                             "data": serialized_requirements.data,
                                                             "file_path": file_path})
        else:
            current_task.update_state(state="FAILURE",
                                      meta={"error": "Failed to save requirements", "file_path": file_path})
    except Exception as e:
        logger.error("Failed to generate requirements: %s", str(e))
        current_task.update_state(
            state="FAILURE",
            meta={
                "error": str(e),
                "exc_type": type(e).__name__,
                "file_path": file_path,
            }
        )
