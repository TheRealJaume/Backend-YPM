from celery.result import AsyncResult
from django.db import transaction
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from project.projects.models import Project
from project.task.models import ProjectTask
from project.task.responses import ProjectTaskResponses
from project.task.serializers import TaskProjectSerializer, TaskUpdateSerializer
from project.task.utils import get_ai_server_request, serialize_project_tasks, \
    save_assignment_in_database, save_estimation_in_database, save_tasks_in_database
import requests
from project.tasks import request_project_tasks


class ProjectTaskFilter:

    def filter_queryset(self, request, queryset, view):
        return queryset.filter(project=request.GET['project'])


class TaskViewset(viewsets.ModelViewSet):
    queryset = ProjectTask.objects.all()
    lookup_field = 'id'
    serializer_class = TaskProjectSerializer
    serializer_action_classes = {
        # "list": TaskListSerializer,
        "update": TaskUpdateSerializer,
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
        # Manage the request to AI celery function
        # request_data = get_ai_server_request(request.data)
        if request.data['action'] == 'create':
            if request.data['target'] == 'project':
                # Llamar a la tarea de manera asíncrona
                task = request_project_tasks.delay(request.data['project'])
        return Response(ProjectTaskResponses.CreateProjectTask200({"task_id": task.id}), 200)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        project_task = ProjectTask.objects.filter(id=kwargs['id'])
        if project_task.exists():
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(data=request.data)
            is_valid = serializer.is_valid()
            if is_valid:
                serializer.update(instance=project_task.first(), validated_data=serializer.validated_data)
                return Response(ProjectTaskResponses.UpdateProjectTask200(),
                                200)
            else:
                return Response(ProjectTaskResponses.UpdateProjectTask400(error=serializer.errors), 400)
        else:
            return Response(ProjectTaskResponses.UpdateProjectTask404(error="Project task not found"),
                            404)

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        project_task = ProjectTask.objects.filter(id=kwargs['id'])
        if project_task.exists():
            project_task.delete()
            return Response(ProjectTaskResponses.DeleteProjectTask200(), 200)
        else:
            return Response(ProjectTaskResponses.DeleteProjectTask404(
                error=f"Project task {kwargs['id']} does not exists"),
                404)

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

    @action(detail=False, methods=['post'])
    def task_status(self, request):
        result = AsyncResult(request.data['task_id'])
        response_data = {
            "task_id": request.data['task_id'],
            "status": result.status,
            "result": result.result if result.status == "SUCCESS" else None
        }
        return Response(ProjectTaskResponses.CheckStatusProjectTask200(response_data), 200)