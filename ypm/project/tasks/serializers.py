from rest_framework import serializers

from project.tasks.models import ProjectTask


# GENERIC
class TaskProjectSerializer(serializers.ModelSerializer):
    """
    This serializer renders all the information from the ProjectTask model
    """

    class Meta:
        model = ProjectTask
        fields = ['name']


# ESTIMATE TASK
class AITaskEstimationSerializer(serializers.ModelSerializer):
    """
    This serializer is used to request for task estimation to AI server
    """

    class Meta:
        model = ProjectTask
        fields = ['id', 'name', 'description']
