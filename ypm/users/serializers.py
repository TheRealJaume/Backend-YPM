import logging
from rest_framework import serializers

from users.jira.models import JiraUser
from users.models import User

logger = logging.getLogger(__name__)


# User
# Retrieve
class UserRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "is_active", "role"]


# Me (personal information)
class UserMeRetrieveSerializer(serializers.ModelSerializer):

    jira = serializers.SerializerMethodField("get_jira_user_info")

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "onboarding", "companies", "jira"]

    def get_jira_user_info(self, user):
        try:
            jira_user = JiraUser.objects.get(user=user)
            return {
                "username": jira_user.username,
                "url": jira_user.url,
                "token": jira_user.token,
            }
        except Exception as e:
            logger.error(f"Error retrieving JIRA user info: {e}")
            return None