from rest_framework import serializers

from company.workers.models import Worker
from project.projects.models import Project
from project.workers.models import ProjectWorker

# PROJECT WORKER

# GENERIC


class ProjectWorkerSerializer(serializers.ModelSerializer):
    """
    This serializer renders all the information from the ProjectWorker model
    """

    class Meta:
        model = ProjectWorker
        fields = "__all__"


# CREATE
class ProjectWorkerCreateSerializer(serializers.ModelSerializer):
    """
    This serializer is used to handle creation of project's technologies
    """

    class Meta:
        model = ProjectWorker
        fields = ["worker", "project"]

    def validate(self, data):
        # TODO: Check if the department is already associated to this project.
        return True

    def create(self, validated_data):
        workers = validated_data.pop("workers")
        for worker in workers:
            project_worker = ProjectWorker(worker=Worker.objects.get(id=worker),
                                           project=Project.objects.get(id=validated_data["project"]))
            project_worker.save()


# RETRIEVE
class ProjectWorkerRetrieveSerializer(serializers.ModelSerializer):
    """
    This serializer is used to handle creation of project technologies
    """

    class Meta:
        model = ProjectWorker
        fields = ["project", "Worker"]


# LIST
class ProjectWorkerListSerializer(serializers.ModelSerializer):
    """
    This serializer is used to list the project technologies
    """

    class Meta:
        model = ProjectWorker
        fields = ["name", "description"]
