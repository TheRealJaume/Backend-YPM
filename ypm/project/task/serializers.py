from rest_framework import serializers

from project.task.models import ProjectTask, ProjectTaskWorker


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


# ASSIGN TASK
class AITaskAssignmentSerializer(serializers.ModelSerializer):
    """
    This serializer is used to request for task estimation to AI server
    """

    class Meta:
        model = ProjectTask
        fields = ['id', 'name', 'description']


# PROJECT TASK WORKERS
class ProjectTaskWorkerSerializer(serializers.ModelSerializer):
    """
    This serializer is used to serialize project tasks workers basic information
    """
    id = serializers.CharField(source="worker.id")
    first_name = serializers.CharField(source="worker.first_name")
    last_name = serializers.CharField(source="worker.last_name")

    class Meta:
        model = ProjectTaskWorker
        fields = ['id', 'first_name', 'last_name']
