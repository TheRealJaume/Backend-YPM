from django.db import transaction
from jira import JIRA
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from project.jira.models import ProjectJira
from project.jira.responses import ProjectJiraResponses
from project.jira.serializers import ProjectJiraSerializer
from project.jira.utils import create_jira_tasks_list
from project.projects.models import Project
from project.task.models import ProjectTask
from users.jira.models import JiraUser


class ProjectJiraFilter:

    def filter_queryset(self, request, queryset, view):
        return queryset


class ProjectJiraViewset(viewsets.ModelViewSet):
    queryset = ProjectJira.objects.all()
    lookup_field = 'id'
    serializer_class = ProjectJiraSerializer
    serializer_action_classes = {
        # "list": TaskListSerializer,
        # "update": TaskUpdateSerializer,
        # "retrieve": RetrieveTaskSerializer,
        # "create": CreateTaskSerializer,
        # "info": InfoTaskSerializer,
    }
    filter_backends = [
        # UserRoleUserQueryset,
        ProjectJiraFilter, SearchFilter, OrderingFilter]
    permission_classes = [
        # UserPermission,
        IsAuthenticated]

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            super().get_serializer_class()

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        # Save the Jira Project information in the database
        project_jira_instance = ProjectJira.objects.create(project=Project.objects.get(id=request.data['project']),
                                                           name=request.data['name'],
                                                           key=request.data['key'])
        # Return the created instance
        serializer = ProjectJiraSerializer(project_jira_instance)
        return Response(ProjectJiraResponses.CreateProjectJira200(serializer.data), 200)

    @action(detail=False, methods=['get'])
    def remote(self, request, *args, **kwargs):
        # Initialize the list of remote projects
        jira_projects = []
        try:
            # Get jira user information
            jira = JiraUser.objects.get(user=request.user)
            connection = JIRA(server=jira.url, basic_auth=(jira.username, jira.token))
            remote_projects = connection.projects()
            for project in remote_projects:
                jira_projects.append({"key": project.key, "name": project.name})
            return Response(ProjectJiraResponses.ListRemoteJiraProjects200(jira_projects), 200)
        except Exception as e:
            print(f"Error retrieving JIRA user info: {e}")
            return Response(ProjectJiraResponses.ListRemoteJiraProjects500(), 500)

    @action(detail=False, methods=['post'])
    def export_tasks(self, request, *args, **kwargs):
        # Conexión con Jira
        jira = JiraUser.objects.get(user=request.user)
        connection = JIRA(server=jira.url, basic_auth=(jira.username, jira.token))
        # Get the jira project id
        try:
            jira_project = ProjectJira.objects.get(id=request.data['jira_project'])
        except ProjectJira.DoesNotExist:
            return Response(ProjectJiraResponses.ExportJiraTasks204(), 204)
        # Get the list of tasks for the project
        tasks = ProjectTask.objects.filter(project__id=request.data['project'])
        # Create a list of tasks for Jira
        tasks_list = create_jira_tasks_list(tasks, jira_project)
        try:
            connection.create_issues(field_list=tasks_list)
            return Response(ProjectJiraResponses.ExportJiraTasks200(), 200)
        except Exception as e:
            print(f"Error al crear la tarea en Jira: {e}")
            return Response(ProjectJiraResponses.ExportJiraTasks400(), 400)
