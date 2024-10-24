from rest_framework import serializers

from project.projects.models import Project
from project.technologies.models import ProjectTechnology
from technologies.models import Technology


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


# PROJECT TASK
class ProjectTechnologyTaskSerializer(serializers.ModelSerializer):
    """
    This serializer is used to handle creation of project's technologies with tasks
    """
    name = serializers.CharField(source='technology.name', read_only=True)

    class Meta:
        model = ProjectTechnology
        fields = ["name"]
