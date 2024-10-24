from project.departments.models import ProjectDepartment
from project.projects.models import Project
from project.tasks.serializers import TaskProjectSerializer
from ypm import settings


def get_ai_server_request(data, num_tasks=3):
    """
    This function is used to retrieve the AI server request.
    """
    if data['target'] == 'project':
        try:
            project = Project.objects.get(id=data['project'])
            data = TaskProjectSerializer(project).data
        except Exception as e:
            return str(e)
        return {
            'url': settings.AI_SERVER_URL + "/tasks/project/",
            'data': data
        }

