from rest_framework import serializers

from project.departments.models import ProjectDepartment
from project.departments.serializers import ProjectDepartmentTaskSerializer
from project.projects.models import Project
from project.tasks.models import ProjectTask


# TASK PROJECT

# PROJECT
from project.technologies.models import ProjectTechnology
from project.technologies.serializers import ProjectTechnologyTaskSerializer
from project.workers.models import ProjectWorker
from project.workers.serializers import ProjectWorkerTaskSerializer


class TaskProjectSerializer(serializers.ModelSerializer):
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
            return ProjectTechnologyTaskSerializer(ProjectTechnology.objects.filter(project__id=project.id), many=True).data
        except Exception as e:
            return str(e)

    def get_project_workers(self, project):
        try:
            return ProjectWorkerTaskSerializer(ProjectWorker.objects.filter(project__id=project.id), many=True).data
        except Exception as e:
            return str(e)

    def get_project_departments(self, project):
        try:
            return ProjectDepartmentTaskSerializer(ProjectDepartment.objects.filter(project__id=project.id), many=True).data
        except Exception as e:
            return str(e)

    def get_project_company(self, project):
        try:
            return {"name": project.company.name, "description": project.company.description}
        except Exception as e:
            return str(e)
