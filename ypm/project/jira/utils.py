def create_jira_tasks_list(tasks, project):
    jira_tasks_list = []
    for task in tasks:
        issue_dict = {
            'project': project.key,
            'summary': task.name,
            'description': task.description,
            'issuetype': {'name': "Task"},
        }
        jira_tasks_list.append(issue_dict)
    return jira_tasks_list
