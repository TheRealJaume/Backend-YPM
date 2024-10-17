from django.db import transaction
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from company.workers.models import Worker
from company.workers.responses import WorkerResponses
from company.workers.serializers import WorkerSerializer, CreateWorkerSerializer, ListWorkerSerializer


class WorkerViewset(viewsets.ModelViewSet):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer
    serializer_action_classes = {
        "create": CreateWorkerSerializer,
        "list": ListWorkerSerializer
        # "retrieve": RetrieveWorkerSerializer
        # "update": UpdateWorkerSerializer
    }
    filter_backends = [
        # UserRoleWorkerQueryset,
        SearchFilter, OrderingFilter]
    permission_classes = [
        # WorkerUserPermission,
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
            return Response(WorkerResponses.CreateWorker200(), 200)
        else:
            return Response(WorkerResponses.CreateWorker400(error=serializer.errors), 400)