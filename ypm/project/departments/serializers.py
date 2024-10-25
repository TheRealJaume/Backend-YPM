from rest_framework import serializers

from company.department.models import Department
from project.departments.models import ProjectDepartment
from project.projects.models import Project

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
        project = Project.objects.get(id=validated_data['project'])
        for department_name in validated_data['departments']:
            department = Department.objects.get(name=department_name)
            project_department = ProjectDepartment(project=project,
                                                   department=department)
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


# INFO
class ProjectDepartmentInfoSerializer(serializers.ModelSerializer):
    """
    This serializer is used to retrieve project department information
    """
    name = serializers.CharField(source='department.name', read_only=True)
    description = serializers.CharField(source='department.description', read_only=True)

    class Meta:
        model = ProjectDepartment
        fields = ["name", "description"]


# AI PROJECT TASK
class AIProjectDepartmentTaskSerializer(serializers.ModelSerializer):
    """
    This serializer is used to handle project department tasks
       """
    name = serializers.CharField(source='department.name', read_only=True)

    class Meta:
        model = ProjectDepartment
        fields = ["name"]
