from rest_framework import serializers

from company.workers.models import Worker, WorkerTechnology
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


# INFO
class ProjectWorkerInfoSerializer(serializers.ModelSerializer):
    """
    This serializer renders basic information about the ProjectWorker model
    """
    first_name = serializers.CharField(source='worker.first_name', read_only=True)
    last_name = serializers.CharField(source='worker.last_name', read_only=True)

    class Meta:
        model = ProjectWorker
        fields = ["first_name", "last_name"]


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
    id = serializers.CharField(source="worker.id")
    first_name = serializers.CharField(source="worker.first_name")
    last_name = serializers.CharField(source="worker.last_name")
    time = serializers.CharField(source="worker.time")
    level = serializers.CharField(source="worker.level")

    class Meta:
        model = ProjectWorker
        fields = ["id", "first_name", "last_name", "time", "level"]


# AI PROJECT TASK
class AIProjectWorkerTaskSerializer(serializers.ModelSerializer):
    """
    This serializer renders basic information about the ProjectWorker model
    """

    first_name = serializers.CharField(source="worker.first_name")
    last_name = serializers.CharField(source="worker.last_name")

    class Meta:
        model = ProjectWorker
        fields = ["first_name", "last_name"]


# AI PROJECT WORKER
class AIProjectWorkerSerializer(serializers.ModelSerializer):
    """
    This serializer renders basic information about the ProjectWorker model
    """
    id = serializers.CharField(source="worker.id")
    level = serializers.CharField(source="worker.level")
    technologies = serializers.SerializerMethodField("get_worker_technologies")

    class Meta:
        model = ProjectWorker
        fields = ["id", "level", "technologies"]

    def get_worker_technologies(self, project_worker):
        try:
            return list(WorkerTechnology.objects.filter(worker=project_worker.worker).values_list("technology__name", flat=True))
        except Exception as e:
            return str(e)
