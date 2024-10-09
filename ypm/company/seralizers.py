from rest_framework import serializers

from company.models import Company


# COMPANY
# GENERIC
class CompanySerializer(serializers.ModelSerializer):
    """
    This serializer renders all the information from the Event model
    """

    class Meta:
        model = Company
        fields = "__all__"


# CREATE
class CreateCompanySerializer(serializers.ModelSerializer):
    """
    This serializer is used to handle creation of events
    """

    class Meta:
        model = Company
        fields = ["name", "description"]
