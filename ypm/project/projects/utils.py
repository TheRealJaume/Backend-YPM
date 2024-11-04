from django.db import transaction

from project.projects.models import ProjectRequirement


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
