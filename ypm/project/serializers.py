from rest_framework import serializers

from company.company.models import Company
from project.models import Project, ProjectTechnology


# PROJECT

# GENERIC
from technologies.models import Technology


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
        fields = ["name", "description", "company"]


# PROJECT TECHNOLOGY

# GENERIC
class ProjectTechnologySerializer(serializers.ModelSerializer):
    """
    This serializer renders all the information from the ProjectTechnology model
    """

    class Meta:
        model = ProjectTechnology
        fields = "__all__"


# CREATE
class ProjectTechnologyCreateSerializer(serializers.ModelSerializer):
    """
    This serializer is used to handle creation of project's technologies
    """

    class Meta:
        model = ProjectTechnology
        fields = ["project", "technology"]

    def validate(self, data):
        # TODO: Check if the department is already associated to this project.
        return True

    def create(self, validated_data):
        technologies = validated_data.pop("technologies")
        for technology in technologies:
            project_technology = ProjectTechnology(technology=Technology.objects.get(name=technology),
                                                   project=Project.objects.get(id=validated_data["project"]))
            project_technology.save()


# RETRIEVE
class ProjectTechnologyRetrieveSerializer(serializers.ModelSerializer):
    """
    This serializer is used to handle creation of project technologies
    """

    class Meta:
        model = ProjectTechnology
        fields = ["project", "technology"]


# LIST
class ProjectTechnologyListSerializer(serializers.ModelSerializer):
    """
    This serializer is used to list the project technologies
    """

    class Meta:
        model = ProjectTechnology
        fields = ["name", "description"]
