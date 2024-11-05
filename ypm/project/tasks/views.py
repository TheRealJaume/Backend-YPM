import os

import requests
from django.db import transaction
from jira import JIRA
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from project.projects.models import Project
from project.tasks.models import ProjectTask
from project.tasks.responses import ProjectTaskResponses
from project.tasks.serializers import TaskProjectSerializer
from project.tasks.utils import get_ai_server_request, save_tasks_in_database, serialize_project_tasks, \
    save_assignment_in_database, save_estimation_in_database


class ProjectTaskFilter:

    def filter_queryset(self, request, queryset, view):
        return queryset.filter(project=request.GET['project'])


class TaskViewset(viewsets.ModelViewSet):
    queryset = ProjectTask.objects.all()
    lookup_field = 'id'
    serializer_class = TaskProjectSerializer
    serializer_action_classes = {
        # "list": TaskListSerializer,
        # "update": TaskUpdateSerializer,
        # "retrieve": RetrieveTaskSerializer,
        # "create": CreateTaskSerializer,
        # "info": InfoTaskSerializer,
    }
    filter_backends = [
        # UserRoleUserQueryset,
        ProjectTaskFilter, SearchFilter, OrderingFilter]
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
        # Manage the request to AI server
        ai_request = get_ai_server_request(request.data)
        # Send the request to AI server
        response = requests.post(ai_request['url'], json=ai_request['data'])
        # Check if the request to AI server was successful
        if response.status_code == 200:
            # Get the response from AI server
            response_data = response.json()['data']
            # Save the information in database
            saved, message = save_tasks_in_database(task_info=response_data, project=request.data['project'])
            if saved:
                project = Project.objects.get(id=request.data['project'])
                serialized_tasks = serialize_project_tasks(project)
                return Response(ProjectTaskResponses.CreateProjectTask200(serialized_tasks), 200)
            else:
                return Response(ProjectTaskResponses.CreateProjectTask400(error=message), 400)

    @action(detail=False, methods=['post'])
    def estimate(self, request, *args, **kwargs):
        # Manage the request to AI server
        ai_request = get_ai_server_request(request.data)
        # Send the request to AI server
        response = requests.post(ai_request['url'], json=ai_request['data'])
        # Check if the request to AI server was successful
        if response.status_code == 200:
            # Get the response from AI server
            response_data = response.json()['data']
            # Save the information in database
            saved, message = save_estimation_in_database(task_info=response_data)
            if saved:
                project = Project.objects.get(id=request.data['project'])
                serialized_tasks = serialize_project_tasks(project)
                return Response(ProjectTaskResponses.ProjectTasksEstimation200(serialized_tasks), 200)
            else:
                return Response(ProjectTaskResponses.ProjectTasksEstimation204(), 400)

    @action(detail=False, methods=['post'])
    def assign(self, request, *args, **kwargs):
        # Manage the request to AI server
        ai_request = get_ai_server_request(request.data)
        # Send the request to AI server
        response = requests.post(ai_request['url'], json=ai_request['data'])
        # Check if the request to AI server was successful
        if response.status_code == 200:
            # Get the response from AI server
            response_data = response.json()['data']
            # Save the information in database
            saved, message = save_assignment_in_database(task_info=response_data)
            if saved:
                project = Project.objects.get(id=request.data['project'])
                serialized_tasks = serialize_project_tasks(project)
                return Response(ProjectTaskResponses.ProjectTasksEstimation200(serialized_tasks), 200)
            else:
                return Response(ProjectTaskResponses.ProjectTasksEstimation204(), 400)