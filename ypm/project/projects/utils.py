def get_jira_project(project_name, connection):
    project = None
    for p in connection.projects():
        if p.name == project_name:
            project = p
            break
    return project
