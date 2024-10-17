from django.db import transaction
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


# PROJECT DEPARTMENT
from project.departments.models import ProjectDepartment
from project.departments.serializers import ProjectDepartmentSerializer, ProjectDepartmentCreateSerializer


class ProjectDepartmentViewset(viewsets.ModelViewSet):
    queryset = ProjectDepartment.objects.all()
    lookup_field = 'id'
    serializer_class = ProjectDepartmentSerializer
    serializer_action_classes = {
        # "list": ProjectDepartmentListSerializer,
        # "update": ProjectDepartmentUpdateSerializer,
        # "retrieve": ProjectDepartmentRetrieveSerializer,
        "create": ProjectDepartmentCreateSerializer,
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
            return Response(ProjectDepartmentResponses.CreateProjectDepartment200(), 200)
        else:
            return Response(ProjectDepartmentResponses.CreateProjectDepartment400(error=serializer.errors), 400)
