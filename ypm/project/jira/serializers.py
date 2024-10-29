from rest_framework import serializers

from project.jira.models import ProjectJira


# PROJECT JIRA

# GENERIC
class ProjectJiraSerializer(serializers.ModelSerializer):
    """
    This serializer renders all the information from the JiraProject model
    """

    class Meta:
        model = ProjectJira
        fields = ['id', 'name']
