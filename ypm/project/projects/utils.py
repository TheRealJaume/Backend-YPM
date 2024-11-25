from django.db import transaction
import json

from project.requirements.models import ProjectRequirement


def get_jira_project(project_name, connection):
    project = None
    for p in connection.projects():
        if p.name == project_name:
            project = p
            break
    return project


@transaction.atomic
def save_requirements_in_database(requirements, project):
    try:
        for requirement in requirements['requirements']:
            requirement = ProjectRequirement(requirement=requirement['requirement'], project=project)
            requirement.save()
        return True, "OK"
    except Exception as e:
        return False, str(e)


@transaction.atomic
def save_requirements_from_text_file(requirements, project):
    try:
        requirements_list = json.loads(requirements)['requirements']
        for requirement in requirements_list:
            requirement = ProjectRequirement(requirement=requirement, project=project)
            requirement.save()
        return True, "OK"
    except Exception as e:
        return False, str(e)
