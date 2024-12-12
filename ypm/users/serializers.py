import logging
from rest_framework import serializers

from payments.coins.models import UserCoin
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
    coins = serializers.SerializerMethodField("get_user_coins")

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "onboarding", "companies", "jira", "coins"]

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

    def get_user_coins(self, user):
        try:
            user_coins = UserCoin.objects.get(user=user)
            return user_coins.coins
        except Exception as e:
            logger.error(f"Error retrieving JIRA user info: {e}")
            return None