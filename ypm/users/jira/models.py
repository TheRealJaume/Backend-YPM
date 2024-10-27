from django.db import models
from model_utils.models import SoftDeletableModel, TimeStampedModel, UUIDModel


class JiraUser(UUIDModel, SoftDeletableModel, TimeStampedModel):
    """ Model representing the jira profile connected to the user """
    token = models.CharField(max_length=240, null=False, blank=False)
    username = models.CharField(max_length=255, null=False, blank=False)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, db_column="user")
    url = models.URLField()

    def __str__(self):
        return self.user.email

    class Meta:
        db_table = "users_user_jira"
