from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.decorators import action

from project.task.models import ProjectTask
from ypm_ai.tasks.managers.assign_tasks import TaskAssignmentManager
from ypm_ai.tasks.managers.create_tasks import ProjectTaskManager
from ypm_ai.tasks.managers.estimate_tasks import TaskEstimationManager
from ypm_ai.tasks.responses import TaskResponses
from ypm_ai.tasks.serializers import TaskSerializer


class TaskViewset(viewsets.ModelViewSet):
    queryset = ProjectTask.objects.all()
    lookup_field = 'id'
    serializer_class = TaskSerializer
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
        # IsAuthenticated
    ]

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            super().get_serializer_class()

    @action(detail=False, methods=['post'])
    def project(self, request, *args, **kwargs):
        # Create the manager instance
        manager = ProjectTaskManager(company_name=request.data['company']['name'],
                                     company_definition=request.data['company']['description'],
                                     project_definition=request.data['description'],
                                     project_technologies=", ".join(
                                         [item['name'] for item in request.data['technologies']]),
                                     project_departments=", ".join(
                                         [item['name'] for item in request.data['departments']]),
                                     project_requirements=request.data['requirements'],
                                     num_tasks_per_department=1,
                                     num_tasks_per_phase=1,
                                     num_subtasks_per_department=1,
                                     excel_file=False)
        response = manager.generate_project_tasks()
        return Response(TaskResponses.CreateTask200(data=response), 200)

    @action(detail=False, methods=['post'])
    def department(self, request, *args, **kwargs):
        # Get serializer class
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        # Check if the information sent is valid
        is_valid = serializer.validate(data=request.data)
        if is_valid:
            task = serializer.create(validated_data=request.data)
            return Response(TaskResponses.CreateTask200({"id": task.id}), 200)
        else:
            return Response(TaskResponses.CreateTask400(error=serializer.errors), 400)

    @action(detail=False, methods=['post'])
    def new_task(self, request, *args, **kwargs):
        # Get serializer class
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        # Check if the information sent is valid
        is_valid = serializer.validate(data=request.data)
        if is_valid:
            task = serializer.create(validated_data=request.data)
            return Response(TaskResponses.CreateTask200({"id": task.id}), 200)
        else:
            return Response(TaskResponses.CreateTask400(error=serializer.errors), 400)

    @action(detail=False, methods=['post'])
    def estimate(self, request, *args, **kwargs):
        # Create the manager instance
        manager = TaskEstimationManager(project_tasks=request.data,
                                        excel_file=False)
        response = manager.estimate_project_tasks()
        return Response(TaskResponses.CreateTask200(data=response), 200)

    @action(detail=False, methods=['post'])
    def assign(self, request, *args, **kwargs):
        # Create the manager instance
        manager = TaskAssignmentManager(project_tasks=request.data['tasks'], project_workers=request.data['workers'],
                                        excel_file=False)
        response = manager.assign_project_tasks()
        return Response(TaskResponses.CreateTask200(data=response), 200)

