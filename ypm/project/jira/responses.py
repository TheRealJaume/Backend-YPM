# PROJECT TASK
class ProjectJiraResponses:
    success_template: dict = {"response": {"message_code": "", "code": ""}, "data": ""}
    failed_template: dict = {"response": {"message_code": "", "code": ""}, "error": ""}

    @staticmethod
    def fill_failed_responses(message_code, error, code):
        response = ProjectJiraResponses.failed_template
        response["response"]["message_code"] = message_code
        response["response"]["code"] = code
        response["error"] = error
        return response

    @staticmethod
    def fill_success_responses(message_code, data, code):
        response = ProjectJiraResponses.success_template
        response["response"]["message_code"] = message_code
        response["response"]["code"] = code
        response["data"] = data
        return response

    @staticmethod
    def CreateProjectJira200(data="None"):
        return ProjectJiraResponses.fill_success_responses(message_code=1,  # "ProjectTask created successfully",
                                                           data=data,
                                                           code=200)

    @staticmethod
    def CreateProjectJira400(error="None"):
        return ProjectJiraResponses.fill_failed_responses(message_code=2,
                                                          # "Data sent is not valid to create a ProjectTask",
                                                          error=error,
                                                          code=400)

    @staticmethod
    def ListRemoteJiraProjects500(error="None"):
        return ProjectJiraResponses.fill_failed_responses(message_code=3,
                                                          # "Data sent is not valid to create a ProjectTask",
                                                          error=error,
                                                          code=500)

    @staticmethod
    def ListRemoteJiraProjects200(data="None"):
        return ProjectJiraResponses.fill_success_responses(message_code=4,
                                                           # "Data sent is not valid to create a ProjectTask",
                                                           data=data,
                                                           code=200)
