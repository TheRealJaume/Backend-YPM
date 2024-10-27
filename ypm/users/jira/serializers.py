from rest_framework import serializers

from users.jira.models import JiraUser


# JIRA USER

# GENERIC
class JiraUserSerializer(serializers.ModelSerializer):
    """
    This serializer renders all the information from the JiraUser model
    """

    class Meta:
        model = JiraUser
        fields = "__all__"


# CREATE
class JiraUserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = JiraUser
        fields = ["token", "username", "user", "url"]

    def validate(self, data):
        # TODO: Hacer una peticion al api de jira para comprobar que los datos conectan a una cuenta .
        return True
