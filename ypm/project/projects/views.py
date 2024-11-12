import requests
from django.db import transaction

from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

# PROJECT
from project.projects.models import Project, ProjectRequirement
from project.projects.responses import ProjectResponses, ProjectRequirementResponses
from project.projects.serializers import ProjectSerializer, ProjectListSerializer, RetrieveProjectSerializer, \
    CreateProjectSerializer, InfoProjectSerializer, ProjectRequirementSerializer
from project.projects.utils import save_requirements_in_database
from project.task.utils import serialize_project_tasks, get_ai_server_request


class UserFilterQueryset:
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(company__owner=request.user)


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
        UserFilterQueryset,
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


class ProjectRequirementViewset(viewsets.ModelViewSet):
    queryset = ProjectRequirement.objects.all()
    lookup_field = 'id'
    serializer_class = ProjectRequirementSerializer
    serializer_action_classes = {
        # "list": ProjectListSerializer,
        # "update": ProjectUpdateSerializer,
        # "retrieve": RetrieveProjectSerializer,
        # "create": CreateProjectSerializer,
        # "info": InfoProjectSerializer,
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
        data = request.data
        print(data)
        # Manage the request to AI server (Transcribe audio)
        transcribe_request = get_ai_server_request(request.data)
        # Send the request to AI server
        transcribe_response = requests.post(url=transcribe_request['url'], files={'file': transcribe_request['data']})
        if transcribe_response.status_code == 200:
            # Manage the request to AI server (Get list of requirements)
            requirements_data = {"text": transcribe_response.json()['data'], "action": "summarize"}
            ai_request = get_ai_server_request(requirements_data)
            # Send the request to AI server
            requirements_response = requests.post(url=ai_request['url'], json=ai_request['data'])
            if requirements_response.status_code == 200:
                # Save the requirements in the database
                requirements = requirements_response.json()['data']
                project = Project.objects.get(id=request.data['project'])
                saved, message = save_requirements_in_database(requirements=requirements, project=project)
                if saved:
                    project_requirements = ProjectRequirement.objects.filter(project=project)
                    many = True if project_requirements.count() > 1 else False
                    data = project_requirements if project_requirements.count() > 1 else project_requirements.first()
                    serialized_requirements = ProjectRequirementSerializer(data, many=many)
                    return Response(
                        ProjectRequirementResponses.CreateProjectRequirements200(serialized_requirements.data), 200)
