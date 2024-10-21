from rest_framework import serializers

from company.company.models import Company
from project.projects.models import Project
from project.technologies.models import ProjectTechnology
from project.technologies.serializers import ProjectTechnologySerializer
from project.workers.models import ProjectWorker
from project.workers.serializers import ProjectWorkerSerializer, ProjectWorkerInfoSerializer


# PROJECT

# GENERIC
class ProjectSerializer(serializers.ModelSerializer):
    """
    This serializer renders all the information from the Project model
    """

    class Meta:
        model = Project
        fields = "__all__"


# CREATE
class CreateProjectSerializer(serializers.ModelSerializer):
    """
    This serializer is used to handle creation of projects
    """

    class Meta:
        model = Project
        fields = ["name", "description", "company"]

    def validate(self, data):
        # TODO: Check if the department is already associated to this project.
        return True

    def create(self, validated_data):
        project = Project(name=validated_data['name'], description=validated_data['description'],
                          company=Company.objects.get(id=validated_data['company']))
        project.save()
        return project


# RETRIEVE
class RetrieveProjectSerializer(serializers.ModelSerializer):
    """
    This serializer is used to handle creation of projects
    """

    class Meta:
        model = Project
        fields = ["name", "description", "company"]


# LIST
class ProjectListSerializer(serializers.ModelSerializer):
    """
    This serializer is used to list the projects
    """

    class Meta:
        model = Project
        fields = ["id", "name", "description", "company"]


# DETAIL
class InfoProjectSerializer(serializers.ModelSerializer):
    """
    This serializer is used to list the project details
    """
    workers = serializers.SerializerMethodField("get_project_workers")
    technologies = serializers.SerializerMethodField("get_project_technologies")

    class Meta:
        model = Project
        fields = ["id", "name", "description", "workers", "technologies"]

    def get_project_technologies(self, project):
        try:
            return ProjectTechnologySerializer(ProjectTechnology.objects.filter(project__id=project.id), many=True).data
        except Exception as e:
            return str(e)

    def get_project_workers(self, project):
        try:
            return ProjectWorkerInfoSerializer(ProjectWorker.objects.filter(project__id=project.id), many=True).data
        except Exception as e:
            return str(e)
