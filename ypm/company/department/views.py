from django.db import transaction
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from company.department.models import CompanyDepartment, Department
from company.department.responses import CompanyDepartmentResponses
from company.department.serializers import CreateCompanyDepartmentSerializer, CompanyDepartmentSerializer, \
    DepartmentSerializer, ListDepartmentSerializer


class CompanyDepartmentViewset(viewsets.ModelViewSet):
    queryset = CompanyDepartment.objects.all()
    serializer_class = CompanyDepartmentSerializer
    serializer_action_classes = {
        "create": CreateCompanyDepartmentSerializer,
        # "list": ListCompanyDepartmentSerializer
        # "retrieve": RetrieveCompanyDepartmentSerializer
        # "update": UpdateCompanyDepartmentSerializer
    }
    filter_backends = [
        # UserRoleDepartmentQueryset,
        SearchFilter, OrderingFilter]
    permission_classes = [
        # DepartmentUserPermission,
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
        # Check if the data sent is valid
        is_valid = serializer.validate(data=request.data)
        if is_valid:
            # Check if the information sent is valid
            serializer.create(validated_data=request.data)
            return Response(CompanyDepartmentResponses.CreateCompanyDepartment200(), 200)


class DepartmentViewset(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    serializer_action_classes = {
        # "create": CreateDepartmentSerializer,
        "list": ListDepartmentSerializer
        # "retrieve": RetrieveDepartmentSerializer
        # "update": UpdateDepartmentSerializer
    }
    filter_backends = [
        # UserRoleDepartmentQueryset,
        SearchFilter, OrderingFilter]
    permission_classes = [
        # DepartmentUserPermission,
        IsAuthenticated]

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            super().get_serializer_class()
