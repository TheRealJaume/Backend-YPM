import requests
from django.db import transaction
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from project.tasks.models import ProjectTask
from project.tasks.responses import ProjectTaskResponses
from project.tasks.serializers import TaskProjectSerializer
from project.tasks.utils import get_ai_server_request


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
        # Manage the request to AI server
        ai_request = get_ai_server_request(request.data)
        # Send the request to AI server
        response = requests.post(ai_request['url'], json=ai_request['data'])
        # Check if the request to AI server was successful
        if response.status_code == 200:
            # Get the response from AI server
            response_data = response.json()['data']
            return Response(ProjectTaskResponses.CreateProjectTask200(response_data), 200)
