from rest_framework import serializers

from project.departments.models import ProjectDepartment


# PROJECT

# GENERIC
class ProjectDepartmentSerializer(serializers.ModelSerializer):
    """
    This serializer renders all the information from the ProjectDepartment model
    """

    class Meta:
        model = ProjectDepartment
        fields = "__all__"


# CREATE
class ProjectDepartmentCreateSerializer(serializers.ModelSerializer):
    """
    This serializer is used to handle creation of project departments
    """

    class Meta:
        model = ProjectDepartment
        fields = ["id", "project", "department"]

    def validate(self, data):
        # TODO: Check if the department is already associated to this project.
        return True

    def create(self, validated_data):
        for department in validated_data['departments']:
            project_department = ProjectDepartment(project__id=validated_data['project'],
                                                   department__name=department)
            project_department.save()


# RETRIEVE
class RetrieveProjectDepartmentSerializer(serializers.ModelSerializer):
    """
    This serializer is used to handle creation of project departments
    """

    class Meta:
        model = ProjectDepartment
        fields = ["id", "project", "department"]


# LIST
class ProjectListSerializer(serializers.ModelSerializer):
    """
    This serializer is used to list the project departments
    """

    class Meta:
        model = ProjectDepartment
        fields = ["id", "project", "department"]
