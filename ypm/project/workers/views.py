from django.db import transaction
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from project.workers.models import ProjectWorker
from project.workers.responses import ProjectWorkerResponses
from project.workers.serializers import ProjectWorkerSerializer, ProjectWorkerCreateSerializer

# PROJECT WORKER


class ProjectWorkerViewset(viewsets.ModelViewSet):
    queryset = ProjectWorker.objects.all()
    lookup_field = 'id'
    serializer_class = ProjectWorkerSerializer
    serializer_action_classes = {
        # "list": ProjectWorkerListSerializer,
        # "update": ProjectWorkerUpdateSerializer,
        # "retrieve": ProjectWorkerRetrieveSerializer,
        "create": ProjectWorkerCreateSerializer,
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
            serializer.create(validated_data=request.data)
            return Response(ProjectWorkerResponses.CreateProjectWorker200(), 200)
        else:
            return Response(ProjectWorkerResponses.CreateProjectWorker400(error=serializer.errors), 400)
