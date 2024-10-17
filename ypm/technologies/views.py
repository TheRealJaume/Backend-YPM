from django.db import transaction
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from technologies.models import Technology
from technologies.responses import TechnologyResponses
from technologies.serializers import TechnologySerializer, CreateTechnologySerializer, ListTechnologySerializer


class TechnologyViewset(viewsets.ModelViewSet):
    queryset = Technology.objects.all()
    serializer_class = TechnologySerializer
    serializer_action_classes = {
        # "create": CreateTechnologySerializer,
        "list": ListTechnologySerializer
        # "retrieve": RetrieveTechnologySerializer
        # "update": UpdateTechnologySerializer
    }
    filter_backends = [
        # UserRoleTechnologyQueryset,
        SearchFilter, OrderingFilter]
    permission_classes = [
        # TechnologyUserPermission,
        IsAuthenticated]

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            super().get_serializer_class()

    # @transaction.atomic
    # def create(self, request, *args, **kwargs):
    #     # Get serializer class
    #     serializer_class = self.get_serializer_class()
    #     serializer = serializer_class(data=request.data)
    #     # Check if the information sent is valid
    #     is_valid = serializer.validate(data=request.data)
    #     if is_valid:
    #         serializer.create(validated_data=request.data)
    #         return Response(TechnologyResponses.CreateTechnology200(), 200)
    #     else:
    #         return Response(TechnologyResponses.CreateTechnology400(error=serializer.errors), 400)
