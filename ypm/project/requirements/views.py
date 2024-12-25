import os
import logging
from celery.result import AsyncResult
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db import transaction
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from project.requirements.models import ProjectRequirement
from project.requirements.responses import ProjectRequirementResponses
from project.requirements.serializers import ProjectRequirementSerializer, ProjectRequirementListSerializer, \
    ProjectRequirementUpdateSerializer, ProjectRequirementCreateSerializer
from project.tasks import get_requirements_from_audio, get_requirements_from_text

logger = logging.getLogger('django')

class ProjectRequirementViewset(viewsets.ModelViewSet):
    queryset = ProjectRequirement.objects.all()
    lookup_field = 'id'
    serializer_class = ProjectRequirementSerializer
    serializer_action_classes = {
        "list": ProjectRequirementListSerializer,
        "update": ProjectRequirementUpdateSerializer,
        # "retrieve": RetrieveProjectSerializer,
        "create": ProjectRequirementCreateSerializer,
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
        if 'name' in request.data:
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(data=request.data)
            is_valid = serializer.is_valid()
            if is_valid:
                requirement = serializer.create(serializer.validated_data)
                return Response(ProjectRequirementResponses.CreateProjectRequirements200({"id": requirement.id,
                                                                                         "name": requirement.requirement}), 200)
            else:
                return Response(ProjectRequirementResponses.CreateProjectRequirements400(error=serializer.errors), 400)
        else:
            file_name, file_extension = os.path.splitext(request.data['file'].name)
            if 'file' not in request.data:
                return Response({"error": "No file provided in request"}, 400)

            file = request.data['file']
            print(f"Received file: {file.name}")

            file_path = default_storage.save(f"{file.name}", ContentFile(file.read()))
            url = default_storage.url(file_path)  # Obtén la URL pública del archivo
            print(f"File saved at: {file_path}, URL: {url}")

            if file_extension in ['.txt', '.pdf']:
                print("Analizando requerimientos")
                logger.info("Analizando requerimientos en archivo de texto")
                task = get_requirements_from_text.delay(file_path=file_path, project=request.data['project'])
                return Response(
                    ProjectRequirementResponses.CreateProjectRequirements200({"task_id": task.id}), 200)
            elif file_extension == ['.mp3']:
                try:
                    # Generar una URL para el archivo (local o en S3)
                    task = get_requirements_from_audio.delay(file_path=file_path, project=request.data['project'])
                    return Response(
                        ProjectRequirementResponses.CreateProjectRequirements200({"task_id": task.id}), 200)
                except Exception as e:
                    return Response(ProjectRequirementResponses.CreateProjectRequirements400(error=str(e)), 400)
            else:
                return Response(ProjectRequirementResponses.CreateProjectRequirements400(
                    error="No se ha encontrado un tipo de archivo válido"), 400)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        project_requirement = ProjectRequirement.objects.filter(id=kwargs['id'])
        if project_requirement.exists():
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(data=request.data)
            is_valid = serializer.is_valid()
            if is_valid:
                serializer.update(instance=project_requirement.first(), validated_data=serializer.validated_data)
                return Response(ProjectRequirementResponses.UpdateProjectRequirement200(),
                                200)
            else:
                return Response(ProjectRequirementResponses.UpdateProjectRequirement400(error=serializer.errors), 400)
        else:
            return Response(ProjectRequirementResponses.UpdateProjectRequirement404(error="Project requirement not found"),
                            404)

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        project_task = ProjectRequirement.objects.filter(id=kwargs['id'])
        if project_task.exists():
            project_task.delete()
            return Response(ProjectRequirementResponses.DeleteProjectRequirement200(), 200)
        else:
            return Response(ProjectRequirementResponses.DeleteProjectRequirement404(
                error=f"Project requirement {kwargs['id']} does not exists"),
                404)

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
            normalized_file_path = os.path.normpath(file_path.lstrip('./'))
            full_file_path = os.path.join(settings.MEDIA_ROOT, normalized_file_path)
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
        if result.status == "FAILURE":
            logger.error("Error processing requirements")
            return Response(ProjectRequirementResponses.CheckStatusTranscription400(response_data), 400)
        else:
            return Response(ProjectRequirementResponses.CheckStatusTranscription200(response_data), 200)
