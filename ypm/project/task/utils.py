from company.workers.models import Worker
from project.departments.models import ProjectDepartment
from project.phases.models import ProjectPhase
from project.projects.models import Project
from project.projects.serializers import AITaskProjectSerializer
from project.sprints.models import ProjectSprint
from project.task.models import ProjectTask, ProjectTaskWorker
from project.task.serializers import AITaskEstimationSerializer, AITaskAssignmentSerializer, \
    ProjectTaskWorkerSerializer
from project.workers.models import ProjectWorker
from project.workers.serializers import AIProjectWorkerSerializer
from ypm import settings


def get_ai_server_request(request_data, num_tasks=3):
    """
    This function is used to retrieve the AI server request.
    """
    # TODO: Implementar el solicitar tareas por departamento o fase-departamento
    if request_data['action'] == 'create':
        if request_data['target'] == 'project':
            url = "/tasks/project/"
            try:
                project = Project.objects.get(id=request_data['project'])
                data = AITaskProjectSerializer(project).data
            except Exception as e:
                return {'url': None, 'data': e}
    elif request_data['action'] == 'estimate':
        url = "/tasks/estimate/"
        try:
            project_tasks = ProjectTask.objects.filter(project=request_data['project'])
            many = True if project_tasks.count() > 1 else False
            project_tasks_data = project_tasks if project_tasks.count() > 1 else project_tasks.first()
            data = AITaskEstimationSerializer(project_tasks_data, many=many).data
        except Exception as e:
            return {'url': None, 'data': e}
    elif request_data['action'] == 'assign':
        url = "/tasks/assign/"
        try:
            data = {}
            # Project tasks to be sent
            project_tasks = ProjectTask.objects.filter(project=request_data['project'])
            many = True if project_tasks.count() > 1 else False
            project_tasks_data = project_tasks if project_tasks.count() > 1 else project_tasks.first()
            data['tasks'] = AITaskAssignmentSerializer(project_tasks_data, many=many).data
            # Project workers to be sent
            project_workers = ProjectWorker.objects.filter(project=request_data['project'])
            many = True if project_workers.count() > 1 else False
            project_workers_data = project_workers if project_workers.count() > 1 else project_workers.first()
            data['workers'] = AIProjectWorkerSerializer(project_workers_data, many=many).data
        except Exception as e:
            return {'url': None, 'data': e}
    elif request_data['action'] == 'transcript':
        url = "/project/requirements/transcript/"
        try:
            # Assign the audio file to the data parameter
            data = request_data['file']
        except Exception as e:
            return {'url': None, 'data': e}
    elif request_data['action'] == 'summarize':
        url = "/project/requirements/summarize/"
        try:
            # Assign the audio file to the data parameter
            data = request_data['text']
        except Exception as e:
            return {'url': None, 'data': e}
    else:
        url = None
        data = None
    return data


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
                    project_phase = ProjectPhase.objects.get(name=phase_name, project=project)
                except:
                    project_phase = ProjectPhase.objects.create(name=phase_name, description=phase_name,
                                                                project=project)
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


def save_assignment_in_database(task_info):
    """
    This function is used to save the assigned tasks in the database.
    """
    try:
        for task in task_info['asigned_tasks']:
            project_task = ProjectTask.objects.get(id=task['id'])
            worker = Worker.objects.get(id=task['worker_id'])
            task_worker = ProjectTaskWorker(task=project_task, worker=worker)
            task_worker.save()
        return True, "OK"
    except Exception as e:
        return False, str(e)


def save_estimation_in_database(task_info):
    """
    This function is used to save the assigned tasks in the database.
    """
    try:
        for task in task_info['estimated_tasks']:
            project_task = ProjectTask.objects.get(id=task['id'])
            project_task.time = task['task_estimation']
            project_task.save()
        return True, "OK"
    except Exception as e:
        return False, str(e)


def save_organization_in_database(sprint_info, project):
    """
    This function is used to save the sprints in the database.
    """
    try:
        for sprint in sprint_info['sprint']:
            project_sprint = ProjectSprint(name=sprint['name'], description=sprint['target'], time=sprint['time'],
                                           project=project)
            project_sprint.save()
            for task in sprint['tasks']:
                project_task = ProjectTask.objects.get(id=task['task_id'])
                project_task.sprint = project_sprint
                project_task.save()
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
                # Serialize the project task workers
                task_workers = ProjectTaskWorker.objects.filter(task=task)
                # Create the final dictionary to be sent
                task_dict = {"id": str(task.id), "name": task.name, "description": task.description, "time": task.time}
                if task_workers.count() > 0:
                    task_workers_data = task_workers if task_workers.count() > 1 else task_workers.first()
                    many = True if task_workers.count() > 1 else False
                    worker_dict = ProjectTaskWorkerSerializer(task_workers_data, many=many)
                    task_dict["workers"] = [worker_dict.data]
                phase_dict["tasks"].append(task_dict)
            department_dict["phases"].append(phase_dict)
        project_dict["departments"].append(department_dict)
    return project_dict


def serialize_sprint_tasks(project):
    project_tasks = ProjectTask.objects.filter(project=project)
    project_sprints = ProjectSprint.objects.filter(project=project)
    project_dict = {"project": project.name, "sprints": []}
    for sprint in project_sprints:
        sprint_dict = {"id": str(sprint.id), "name": sprint.name, "description": sprint.description,
                       "time": sprint.time, "tasks": []}
        sprint_tasks = project_tasks.filter(sprint=sprint)
        for sprint_task in sprint_tasks:
                task_dict = {"id": str(sprint_task.id), "name": sprint_task.name, "description": sprint_task.description, "time": sprint_task.time}
                task_workers = ProjectTaskWorker.objects.filter(task=sprint_task)
                if task_workers.count() > 0:
                    task_workers_data = task_workers if task_workers.count() > 1 else task_workers.first()
                    many = True if task_workers.count() > 1 else False
                    worker_dict = ProjectTaskWorkerSerializer(task_workers_data, many=many)
                    task_dict["workers"] = [worker_dict.data]
                sprint_dict["tasks"].append(task_dict)
        project_dict["sprints"].append(sprint_dict)
    return project_dict
