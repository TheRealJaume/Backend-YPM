import logging
from rest_framework import serializers

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
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "onboarding", "companies"]
