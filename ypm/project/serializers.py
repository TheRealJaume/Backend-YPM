from rest_framework import serializers

from company.company.models import Company
from project.models import Project


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
        project_department = Project(name=validated_data['name'], description=validated_data['description'],
                                     company=Company.objects.get(id=validated_data['company']))
        project_department.save()


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
        fields = ["name", "description", "company"]
