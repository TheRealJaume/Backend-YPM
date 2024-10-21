from rest_framework import serializers

from company.company.models import Company
from company.department.models import CompanyDepartment, Department


# DEPARTMENT
# GENERIC
class DepartmentSerializer(serializers.ModelSerializer):
    """
    This serializer renders all the information from the Department model
    """

    class Meta:
        model = Department
        fields = "__all__"


# LIST
class ListDepartmentSerializer(serializers.ModelSerializer):
    """
    This serializer renders a list of departments
    """

    class Meta:
        model = Department
        fields = ["name", "description"]


# COMPANY_DEPARTMENT
# GENERIC
class CompanyDepartmentSerializer(serializers.ModelSerializer):
    """
    This serializer renders all the information from the CompanyDepartment model
    """

    class Meta:
        model = CompanyDepartment
        fields = "__all__"


# RETRIEVE
class RetrieveCompanyDepartmentSerializer(serializers.ModelSerializer):
    """
    This serializer renders all the information from the CompanyDepartment model
    """

    class Meta:
        model = CompanyDepartment
        fields = ["company", "department"]


# LIST
class ListCompanyDepartmentSerializer(serializers.ModelSerializer):
    """
    This serializer renders all the information from the CompanyDepartment model
    """

    class Meta:
        model = CompanyDepartment
        fields = ["company", "department"]


# CREATE
class CreateCompanyDepartmentSerializer(serializers.ModelSerializer):
    """
    This serializer is used to create a new company department
    """

    departments = serializers.ListField(
        child=serializers.CharField(max_length=100)
    )

    class Meta:
        model = CompanyDepartment
        fields = ["departments", "company"]

    def validate(self, data):
        # Check for duplicate department names.
        if len(data) != len(set(data)):
            raise serializers.ValidationError("There are duplicate department names.")
        if not Company.objects.filter(id=data['company']).exists():
            raise serializers.ValidationError("There is no company created to associate these departments.")
        # TODO: Check if the department is already associated to this company.
        return True

    def create(self, validated_data):
        departments = validated_data.pop("departments")
        for department in departments:
            company_department = CompanyDepartment(company=Company.objects.get(id=validated_data['company']),
                                                   department=Department.objects.get(name=department))
            company_department.save()
