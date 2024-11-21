# DJANGO
import os

from django.http import HttpResponse
from openpyxl import Workbook
from io import BytesIO
from celery.result import AsyncResult
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db import transaction
from django.utils.timezone import now
from rest_framework import viewsets, status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

# PROJECT
from project.projects.models import Project, ProjectRequirement
from project.projects.responses import ProjectResponses, ProjectRequirementResponses
from project.projects.serializers import ProjectSerializer, ProjectListSerializer, RetrieveProjectSerializer, \
    CreateProjectSerializer, InfoProjectSerializer, ProjectRequirementSerializer
from project.sprints.models import ProjectSprint
from project.task.models import ProjectTask, ProjectTaskWorker
from project.task.utils import serialize_project_tasks
from project.tasks import get_requirements_from_audio

# AI
from ypm_ai.tasks.managers.project_requirements import RequirementsManager


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

    @action(detail=False, methods=['post'])
    def export_excel(self, request):
        try:
            # Obtain the project and its sprints
            project = Project.objects.get(id=request.data['project'])
            sprints = ProjectSprint.objects.filter(project=project).order_by('start_date')

            # Create the Excel file
            wb = Workbook()
            ws = wb.active
            ws.title = f"Project {project.name}"

            # Write headers
            headers = ['Sprint', 'Task', 'Description', 'Estimation (h)', 'Department', 'Assigned To']
            for col_num, header in enumerate(headers, 1):
                ws.cell(row=1, column=col_num, value=header)

            # Write tasks organized by sprints
            row = 2
            for sprint in sprints:
                tasks = ProjectTask.objects.filter(sprint=sprint)
                for task in tasks:
                    worker = ProjectTaskWorker.objects.filter(task=task)
                    ws.cell(row=row, column=1, value=sprint.name)
                    ws.cell(row=row, column=2, value=task.name)
                    ws.cell(row=row, column=3, value=task.description)
                    ws.cell(row=row, column=4, value=task.time)
                    ws.cell(row=row, column=5, value=task.department.department.name)
                    ws.cell(row=row, column=6, value=worker.first().worker.first_name if worker.count() > 0 else 'Unassigned')
                    row += 1

            # Save the Excel file to memory
            excel_file = BytesIO()
            wb.save(excel_file)
            excel_file.seek(0)

            # Prepare the response
            response = HttpResponse(
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            )
            filename = f"project_{project.id}_tasks_{now().strftime('%Y%m%d%H%M%S')}.xlsx"
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            wb.save(response)
            return response
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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

    def create(self, request, *args, **kwargs):
        try:
            # Temporary solution to store the requirements audio file
            file_path = default_storage.save(f"{request.data['file'].name}", ContentFile(request.data['file'].read()))
            # Generar una URL para el archivo (local o en S3)
            file_url = f"./media/{file_path}"
            task = get_requirements_from_audio.delay(file_path=file_url, project=request.data['project'])
            return Response(
                ProjectRequirementResponses.CreateProjectRequirements200({"task_id": task.id}), 200)
        except Exception as e:
            return Response(ProjectRequirementResponses.CreateProjectRequirements400(error=str(e)), 400)

    @action(detail=False, methods=['post'])
    def requirements_status(self, request):
        task_id = request.data['requirement_id']
        result = AsyncResult(task_id)

        # Verificar el estado y obtener información
        if isinstance(result.info, dict):
            progress = result.info.get("progress")
            message = result.info.get("message")
            file_path = result.info.get("file_path")  # Obtener la ruta del archivo
            data = result.info.get("data")  # Obtener la lista (si existe)
        else:
            progress = None
            message = None
            file_path = None
            data = None

        # Procesar `data` si es una lista
        processed_data = None
        if isinstance(data, list):
            # Procesa la lista (opcional)
            processed_data = [{"requirement": item.get("requirement")} for item in data if "requirement" in item]
        elif data:
            # Si `data` no es una lista pero existe, úsala directamente
            processed_data = data

        # Eliminar el archivo si la tarea está completa
        if result.status in ["SUCCESS", "FAILURE"] and file_path:
            full_file_path = os.path.join(settings.MEDIA_ROOT, file_path)
            if os.path.exists(full_file_path):
                os.remove(full_file_path)
                print(f"Archivo eliminado: {full_file_path}")

        # Respuesta
        response_data = {
            "requirement_id": task_id,
            "status": result.status,
            "progress": progress,
            "message": message,
            "result": processed_data if result.status == "SUCCESS" else None,
        }
        return Response(ProjectRequirementResponses.CheckStatusTranscription200(response_data), 200)
