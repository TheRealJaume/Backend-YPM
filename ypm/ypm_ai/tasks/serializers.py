from rest_framework import serializers

# TASK

# GENERIC
from tasks.models import ProjectTask


class TaskSerializer(serializers.ModelSerializer):
    """
    This serializer renders all the information from the Task model
    """

    class Meta:
        model = ProjectTask
        fields = "__all__"


