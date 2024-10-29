import os

from django.db import transaction
from jira import JIRA

from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

# PROJECT
from project.projects.models import Project
from project.projects.responses import ProjectResponses
from project.projects.serializers import ProjectSerializer, ProjectListSerializer, RetrieveProjectSerializer, \
    CreateProjectSerializer, InfoProjectSerializer
from project.projects.utils import get_jira_project
from project.tasks.utils import serialize_project_tasks


class ProjectViewset(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    lookup_field = 'id'
    serializer_class = ProjectSerializer
    serializer_action_classes = {
        "list": ProjectListSerializer,
        # "update": ProjectUpdateSerializer,
        "retrieve": RetrieveProjectSerializer,
        "create": CreateProjectSerializer,
        "info": InfoProjectSerializer,
    }
    filter_backends = [
        # UserRoleUserQueryset,
        SearchFilter, OrderingFilter]
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
        # Get serializer class
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        # Check if the information sent is valid
        is_valid = serializer.validate(data=request.data)
        if is_valid:
            project = serializer.create(validated_data=request.data)
            return Response(ProjectResponses.CreateProject200({"id": project.id}), 200)
        else:
            return Response(ProjectResponses.CreateProject400(error=serializer.errors), 400)

    @action(detail=False, methods=['get'])
    def info(self, request, *args, **kwargs):
        # Get serializer class
        serializer_class = self.get_serializer_class()
        # Create event statistics
        if 'project' in request.GET:
            try:
                project = Project.objects.get(id=request.GET['project'])
            except Exception:
                return Response(ProjectResponses.DetailProject204(), 204)
            project_serializer = serializer_class(project)
            return Response(ProjectResponses.DetailProject200(project_serializer.data), 200)

    @action(detail=False, methods=['get'])
    def tasks(self, request, *args, **kwargs):
        # Create event statistics
        if 'project' in request.GET:
            try:
                project = Project.objects.get(id=request.GET['project'])
            except Exception:
                return Response(ProjectResponses.ProjectTasks204(), 204)
            serialized_tasks = serialize_project_tasks(project)
            return Response(ProjectResponses.ProjectTasks200(serialized_tasks), 200)

    @action(detail=False, methods=['post'])
    def jira(self, request, *args, **kwargs):
        # Conexión con Jira
        connection = JIRA(server=os.getenv('JIRA_URL'), basic_auth=(os.getenv('JIRA_USERNAME'), os.getenv('JIRA_TOKEN')))
        # Get the jira project id
        project = get_jira_project(project_name=os.getenv('JIRA_PROJECT_NAME'), connection=connection)
        # TODO: Tomar el key desde el objeto ProjectJira
        issue_dict = {
            'project': project.key,
            'summary': "Esta es la prueba que YPM se conecta con JIRA",
            'description': 'Description de la tareas que comprueba que se puede conectar JIRA con YPM',
            'issuetype': {'name': "Task"},
        }

        # Crear la tarea en Jira
        try:
            new_issue = connection.create_issue(fields=issue_dict)
            print(f"Tarea creada en Jira con clave: {new_issue.key}")
            return Response(ProjectResponses.ProjectTasks200(), 200)
        except Exception as e:
            print(f"Error al crear la tarea en Jira: {e}")
            return Response(ProjectResponses.ProjectTasks204(), 204)
