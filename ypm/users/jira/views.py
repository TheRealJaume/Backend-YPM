from django.db import transaction
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


# PROJECT WORKER
from users.jira.models import JiraUser
from users.jira.responses import JiraUserResponses
from users.jira.serializers import JiraUserSerializer, JiraUserCreateSerializer


class JiraUserViewset(viewsets.ModelViewSet):
    queryset = JiraUser.objects.all()
    lookup_field = 'id'
    serializer_class = JiraUserSerializer
    serializer_action_classes = {
        # "list": ProjectWorkerListSerializer,
        # "update": ProjectWorkerUpdateSerializer,
        # "retrieve": ProjectWorkerRetrieveSerializer,
        "create": JiraUserCreateSerializer,
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
        request.data['user'] = request.user
        serializer = serializer_class(data=request.data)
        # Check if the information sent is valid
        is_valid = serializer.validate(data=request.data)
        if is_valid:
            jira_user = serializer.create(validated_data=request.data)
            return Response(JiraUserResponses.CreateJiraUser200({"url": jira_user.url, "username": jira_user.username, "token": jira_user.token}), 200)
        else:
            return Response(JiraUserResponses.CreateJiraUser400(error=serializer.errors), 400)