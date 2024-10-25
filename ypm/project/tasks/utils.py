from project.departments.models import ProjectDepartment
from project.phases.models import ProjectPhase
from project.projects.models import Project
from project.projects.serializers import AITaskProjectSerializer
from project.tasks.models import ProjectTask
from ypm import settings


def get_ai_server_request(data, num_tasks=3):
    """
    This function is used to retrieve the AI server request.
    """
    if data['target'] == 'project':
        try:
            project = Project.objects.get(id=data['project'])
            data = AITaskProjectSerializer(project).data
        except Exception as e:
            return str(e)
        return {
            'url': settings.AI_SERVER_URL + "/tasks/project/",
            'data': data
        }


def save_tasks_in_database(task_info, project):
    """
    This function is used to save the tasks in the database.
    """
    try:
        project = Project.objects.get(id=project)
        for department in task_info['departments']:
            department_name = department['department']
            phases = department['phases']
            for phase in phases:
                phase_name = phase['name']
                try:
                    project_phase = ProjectPhase.objects.get(name=phase_name)
                except:
                    project_phase = ProjectPhase.objects.create(name=phase_name, description=phase_name, project=project)
                tasks = phase['tasks']
                for task in tasks:
                    project_department = ProjectDepartment.objects.get(project=project,
                                                                       department__name=department_name)
                    ProjectTask.objects.create(project=project, name=task['task_name'],
                                               description=task['task_description'],
                                               phase=project_phase, department=project_department)
        return True, "OK"
    except Exception as e:
        return False, str(e)


def serialize_project_tasks(project):
    project_departments = ProjectDepartment.objects.filter(project=project)
    phases = ProjectPhase.objects.filter(project=project)
    project_tasks = ProjectTask.objects.filter(project=project)
    project_dict = {"project": project.name, "departments": []}
    for project_department in project_departments:
        department_dict = {"id": str(project_department.department.id), "name": project_department.department.name,
                           "phases": []}
        for phase in phases:
            phase_dict = {"id": str(phase.id), "name": phase.name, "tasks": []}
            phase_tasks = project_tasks.filter(department=project_department, phase=phase)
            for task in phase_tasks:
                task_dict = {"id": str(task.id), "name": task.name, "description": task.description}
                phase_dict["tasks"].append(task_dict)
            department_dict["phases"].append(phase_dict)
        project_dict["departments"].append(department_dict)
    return project_dict
