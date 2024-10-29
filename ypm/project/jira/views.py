import os

import requests
from django.db import transaction
from jira import JIRA
from requests.auth import HTTPBasicAuth
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from project.jira.models import ProjectJira
from project.jira.responses import ProjectJiraResponses
from project.jira.serializers import ProjectJiraSerializer
from project.projects.models import Project
from project.projects.utils import get_jira_project


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
        # Connection with Jira
        connection = JIRA(server=request.data['url'], basic_auth=(request.data['username'], request.data['token']))
        # Get the Jira project information
        project = get_jira_project(request.data['name'], connection=connection)
        # Save the Jira Project information in the database
        project_jira_instance = ProjectJira.objects.create(project=Project.objects.get(id=request.data['project']),
                                                           name=request.data['name'],
                                                           key=project.key)
        # Return the created instance
        serializer = ProjectJiraSerializer(project_jira_instance)
        return Response(ProjectJiraResponses.CreateProjectJira200(serializer.data), 200)
