from rest_framework import serializers

# COMPANY
# GENERIC
from company.company.models import Company


class CompanySerializer(serializers.ModelSerializer):
    """
    This serializer renders all the information from the Company model
    """

    class Meta:
        model = Company
        fields = "__all__"


# CREATE
class CreateCompanySerializer(serializers.ModelSerializer):
    """
    This serializer is used to handle creation of companies
    """

    class Meta:
        model = Company
        fields = ["name", "description"]

    def create(self, validated_data):
        company = Company(name=validated_data['name'], description=validated_data['description'],
                          owner=validated_data['owner'])
        company.save()
        return company
