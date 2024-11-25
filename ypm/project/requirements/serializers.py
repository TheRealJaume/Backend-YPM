from project.requirements.models import ProjectRequirement
from rest_framework import serializers


# PROJECT REQUIREMENT


class ProjectRequirementSerializer(serializers.ModelSerializer):
    """
    This serializer is used to send the project requirement information
    """

    class Meta:
        model = ProjectRequirement
        fields = ['requirement']


# AI PROJECT REQUIREMENTS
class AIProjectRequirementsSerializer(serializers.ModelSerializer):
    """
    This serializer is used to send the project requirement information
    """

    class Meta:
        model = ProjectRequirement
        fields = ['requirement']


# PROJECT REQUIREMENT LIST
class ProjectRequirementListSerializer(serializers.ModelSerializer):
    """
    This serializer is used to list the project requirements
    """

    name = serializers.CharField(source='requirement')

    class Meta:
        model = ProjectRequirement
        fields = ['id', 'name']


# UPDATE
class ProjectRequirementUpdateSerializer(serializers.ModelSerializer):
    """
    This serializer is used to update project requirement basic information
    """
    name = serializers.CharField(source='requirement')

    class Meta:
        model = ProjectRequirement
        fields = ['name']


# UPDATE
class ProjectRequirementCreateSerializer(serializers.ModelSerializer):
    """
    This serializer is used to create project requirement
    """
    name = serializers.CharField(source='requirement')

    class Meta:
        model = ProjectRequirement
        fields = ['name', 'project']
