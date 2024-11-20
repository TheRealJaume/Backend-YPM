from celery.result import AsyncResult
from django.db import transaction
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from project.projects.models import Project
from project.sprints.models import ProjectSprint
from project.sprints.responses import ProjectSprintResponses
from project.sprints.serializers import ProjectSprintSerializer, AITaskOrganizationSerializer
from project.task.models import ProjectTask
from project.task.serializers import TaskProjectSerializer, TaskUpdateSerializer
from project.task.utils import serialize_project_tasks, save_organization_in_database, serialize_sprint_tasks
from project.tasks import request_project_tasks, request_assign_project_tasks, request_estimate_project_tasks, \
    request_organize_project_tasks

# class ProjectSprintFilter:
#
#     def filter_queryset(self, request, queryset, view):
#         return queryset.filter(project=request.GET['project'])
from ypm_ai.tasks.managers.organize_tasks import TaskOrganizationManager


class ProjectSprintViewset(viewsets.ModelViewSet):
    queryset = ProjectSprint.objects.all()
    lookup_field = 'id'
    serializer_class = ProjectSprintSerializer
    serializer_action_classes = {
        # "update": ProjectSprintUpdateSerializer,
    }
    filter_backends = [
        # ProjectSprintFilter,
        SearchFilter, OrderingFilter]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            super().get_serializer_class()

    # @transaction.atomic
    # def create(self, request, *args, **kwargs):
    #     if request.data['action'] == 'create':
    #         if request.data['target'] == 'project':
    #             # Llamar a la tarea de manera asíncrona
    #             task = request_project_tasks.delay(request.data['project'])
    #     return Response(ProjectSprintResponses.CreateProjectSprint200({"task_id": task.id}), 200)

    # @transaction.atomic
    # def update(self, request, *args, **kwargs):
    #     project_task = ProjectSprint.objects.filter(id=kwargs['id'])
    #     if project_task.exists():
    #         serializer_class = self.get_serializer_class()
    #         serializer = serializer_class(data=request.data)
    #         is_valid = serializer.is_valid()
    #         if is_valid:
    #             serializer.update(instance=project_task.first(), validated_data=serializer.validated_data)
    #             return Response(ProjectSprintResponses.UpdateProjectSprint200(),
    #                             200)
    #         else:
    #             return Response(ProjectSprintResponses.UpdateProjectSprint400(error=serializer.errors), 400)
    #     else:
    #         return Response(ProjectSprintResponses.UpdateProjectSprint404(error="Project task not found"),
    #                         404)
    #
    # @transaction.atomic
    # def destroy(self, request, *args, **kwargs):
    #     project_task = ProjectSprint.objects.filter(id=kwargs['id'])
    #     if project_task.exists():
    #         project_task.delete()
    #         return Response(ProjectSprintResponses.DeleteProjectSprint200(), 200)
    #     else:
    #         return Response(ProjectSprintResponses.DeleteProjectSprint404(
    #             error=f"Project task {kwargs['id']} does not exists"),
    #             404)

    @action(detail=False, methods=['post'])
    def organize(self, request, *args, **kwargs):
        try:
            task = request_organize_project_tasks.delay(request.data['project'])
            return Response(ProjectSprintResponses.ProjectSprintOrganize200({"task_id": task.id}), 200)
        except Exception as e:
            return Response(ProjectSprintResponses.ProjectSprintOrganize400(error=str(e)), 400)

    @action(detail=False, methods=['get'])
    def tasks(self, request, *args, **kwargs):
        project = Project.objects.get(id=request.GET['project'])
        project_tasks = serialize_sprint_tasks(project)
        return Response(ProjectSprintResponses.ProjectSprintTasks200(project_tasks), 200)

    @action(detail=False, methods=['post'])
    def task_status(self, request):
        result = AsyncResult(request.data['task_id'])
        response_data = {
            "task_id": request.data['task_id'],
            "status": result.status,
            "result": result.result if result.status == "SUCCESS" else None
        }
        return Response(ProjectSprintResponses.CheckStatusProjectSprint200(response_data), 200)
