from rest_framework import serializers

from project.sprints.models import ProjectSprint
from project.task.models import ProjectTask, ProjectTaskWorker


# GENERIC
class ProjectSprintSerializer(serializers.ModelSerializer):
    """
    This serializer renders all the information from the ProjectSprint model
    """

    class Meta:
        model = ProjectSprint
        fields = ['project', 'name', 'description', 'start_date', 'end_date']


# AI TASK ORGNAIZATION
class AITaskOrganizationSerializer(serializers.ModelSerializer):
    """
    This serializer is used to request for task estimation to AI server
    """

    worker = serializers.SerializerMethodField('get_task_worker')

    class Meta:
        model = ProjectTask
        fields = ['id', 'name', 'description', 'time', 'worker']

    def get_task_worker(self, task):
        try:
            return ProjectTaskWorker.objects.filter(task=task).first().worker.id
        except Exception as e:
            return str(e)