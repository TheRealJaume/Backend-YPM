from rest_framework import serializers
from technologies.models import Technology


# TECHNOLOGY

# GENERIC
class TechnologySerializer(serializers.ModelSerializer):
    """
    This serializer renders all the information from the technologies model
    """

    class Meta:
        model = Technology
        fields = "__all__"


# CREATE
class CreateTechnologySerializer(serializers.ModelSerializer):
    """
    This serializer is used to handle creation of technologies
    """

    class Meta:
        model = Technology
        fields = ["name", "description", "group"]

    def validate(self, data):
        # TODO: Check if the department is already associated to this Technology.
        return True

    def create(self, validated_data):
        technology = Technology()
        technology.save()


# RETRIEVE
class RetrieveTechnologySerializer(serializers.ModelSerializer):
    """
    This serializer is used to handle creation of technologies
    """

    class Meta:
        model = Technology
        fields = ["name", "description", "group"]


# LIST
class ListTechnologySerializer(serializers.ModelSerializer):
    """
    This serializer is used to list the technologies
    """

    class Meta:
        model = Technology
        fields = ["name", "description", "group"]
