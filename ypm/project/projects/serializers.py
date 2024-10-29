from rest_framework import serializers

from company.company.models import Company
from project.departments.models import ProjectDepartment
from project.departments.serializers import ProjectDepartmentInfoSerializer, AIProjectDepartmentTaskSerializer
from project.jira.models import ProjectJira
from project.projects.models import Project
from project.technologies.models import ProjectTechnology
from project.technologies.serializers import ProjectTechnologySerializer, AIProjectTechnologyTaskSerializer
from project.workers.models import ProjectWorker
from project.workers.serializers import ProjectWorkerInfoSerializer, AIProjectWorkerTaskSerializer


# PROJECT

# GENERIC
class ProjectSerializer(serializers.ModelSerializer):
    """
    This serializer renders all the information from the Project model
    """

    class Meta:
        model = Project
        fields = "__all__"


# CREATE
class CreateProjectSerializer(serializers.ModelSerializer):
    """
    This serializer is used to handle creation of projects
    """

    class Meta:
        model = Project
        fields = ["name", "description", "company"]

    def validate(self, data):
        # TODO: Check if the department is already associated to this project.
        return True

    def create(self, validated_data):
        project = Project(name=validated_data['name'], description=validated_data['description'],
                          company=Company.objects.get(id=validated_data['company']))
        project.save()
        return project


# RETRIEVE
class RetrieveProjectSerializer(serializers.ModelSerializer):
    """
    This serializer is used to handle creation of projects
    """

    class Meta:
        model = Project
        fields = ["name", "description", "company"]


# LIST
class ProjectListSerializer(serializers.ModelSerializer):
    """
    This serializer is used to list the projects
    """

    class Meta:
        model = Project
        fields = ["id", "name", "description", "company"]


# DETAIL
class InfoProjectSerializer(serializers.ModelSerializer):
    """
    This serializer is used to list the project details
    """
    workers = serializers.SerializerMethodField("get_project_workers")
    technologies = serializers.SerializerMethodField("get_project_technologies")
    departments = serializers.SerializerMethodField("get_project_departments")
    jira_project = serializers.SerializerMethodField("get_jira_project")

    class Meta:
        model = Project
        fields = ["id", "name", "description", "workers", "technologies", "departments", "jira_project"]

    def get_project_technologies(self, project):
        try:
            return ProjectTechnologySerializer(ProjectTechnology.objects.filter(project__id=project.id), many=True).data
        except Exception as e:
            return str(e)

    def get_project_workers(self, project):
        try:
            return ProjectWorkerInfoSerializer(ProjectWorker.objects.filter(project__id=project.id), many=True).data
        except Exception as e:
            return str(e)

    def get_project_departments(self, project):
        try:
            return ProjectDepartmentInfoSerializer(ProjectDepartment.objects.filter(project__id=project.id),
                                                   many=True).data
        except Exception as e:
            return str(e)

    def get_jira_project(self, project):
        try:
            return ProjectJira.objects.get(project=project).id
        except Exception as e:
            return None


# Project task serializer for AI
class AITaskProjectSerializer(serializers.ModelSerializer):
    """
    This serializer renders all the information from the Task Project model
    """
    workers = serializers.SerializerMethodField("get_project_workers")
    technologies = serializers.SerializerMethodField("get_project_technologies")
    departments = serializers.SerializerMethodField("get_project_departments")
    company = serializers.SerializerMethodField("get_project_company")

    class Meta:
        model = Project
        fields = ["description", "workers", "technologies", "departments", "company"]

    def get_project_technologies(self, project):
        try:
            return AIProjectTechnologyTaskSerializer(ProjectTechnology.objects.filter(project__id=project.id),
                                                     many=True).data
        except Exception as e:
            return str(e)

    def get_project_workers(self, project):
        try:
            return AIProjectWorkerTaskSerializer(ProjectWorker.objects.filter(project__id=project.id), many=True).data
        except Exception as e:
            return str(e)

    def get_project_departments(self, project):
        try:
            return AIProjectDepartmentTaskSerializer(ProjectDepartment.objects.filter(project__id=project.id),
                                                     many=True).data
        except Exception as e:
            return str(e)

    def get_project_company(self, project):
        try:
            return {"name": project.company.name, "description": project.company.description}
        except Exception as e:
            return str(e)
