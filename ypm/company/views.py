from django.db import transaction
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from company.models import Company
from company.responses import CompanyResponses
from company.seralizers import CompanySerializer, CreateCompanySerializer


class CompanyViewset(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    serializer_action_classes = {
        "create": CreateCompanySerializer,
        # "list": ListCompanySerializer
        # "retrieve": RetrieveCompanySerializer
        # "update": UpdateCompanySerializer
    }
    filter_backends = [
        # UserRoleCompanyQueryset,
        SearchFilter, OrderingFilter]
    permission_classes = [
        # CompanyUserPermission,
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
        is_valid = serializer.is_valid()
        if is_valid:
            serializer.create(validated_data=serializer.validated_data)
            return Response(CompanyResponses.CreateCompany200(), 200)
        else:
            return Response(CompanyResponses.CreateCompany400(error=serializer.errors), 400)
