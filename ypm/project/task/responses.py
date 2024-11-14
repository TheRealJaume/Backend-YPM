# PROJECT TASK
class ProjectTaskResponses:
    success_template: dict = {"response": {"message_code": "", "code": ""}, "data": ""}
    failed_template: dict = {"response": {"message_code": "", "code": ""}, "error": ""}

    @staticmethod
    def fill_failed_responses(message_code, error, code):
        response = ProjectTaskResponses.failed_template
        response["response"]["message_code"] = message_code
        response["response"]["code"] = code
        response["error"] = error
        return response

    @staticmethod
    def fill_success_responses(message_code, data, code):
        response = ProjectTaskResponses.success_template
        response["response"]["message_code"] = message_code
        response["response"]["code"] = code
        response["data"] = data
        return response

    @staticmethod
    def CreateProjectTask200(data="None"):
        return ProjectTaskResponses.fill_success_responses(message_code=1,  # "ProjectTask created successfully",
                                                           data=data,
                                                           code=200)

    @staticmethod
    def CreateProjectTask400(error="None"):
        return ProjectTaskResponses.fill_failed_responses(message_code=2,
                                                          # "Data sent is not valid to create a ProjectTask",
                                                          error=error,
                                                          code=400)

    @staticmethod
    def DetailProjectTask200(data="None"):
        return ProjectTaskResponses.fill_success_responses(message_code=3,  # "ProjectTask created successfully",
                                                           data=data,
                                                           code=200)

    @staticmethod
    def DetailProjectTask204(error="None"):
        return ProjectTaskResponses.fill_failed_responses(message_code=4,
                                                          # "Data sent is not valid to create a ProjectTask",
                                                          error=error,
                                                          code=400)

    @staticmethod
    def ProjectTasksExport200(data="None"):
        return ProjectTaskResponses.fill_success_responses(message_code=5,  # "Project created successfully",
                                                           data=data,
                                                           code=200)

    @staticmethod
    def ProjectTasksExport204(error="None"):
        return ProjectTaskResponses.fill_failed_responses(message_code=6,
                                                          # "Data sent is not valid to create a Project",
                                                          error=error,
                                                          code=204)

    @staticmethod
    def ProjectTasksEstimation200(data="None"):
        return ProjectTaskResponses.fill_success_responses(message_code=7,  # "Project created successfully",
                                                           data=data,
                                                           code=200)

    @staticmethod
    def ProjectTasksEstimation204(error="None"):
        return ProjectTaskResponses.fill_failed_responses(message_code=8,
                                                          # "Data sent is not valid to create a Project",
                                                          error=error,
                                                          code=204)

    @staticmethod
    def CheckStatusProjectTask200(data="None"):
        return ProjectTaskResponses.fill_success_responses(message_code=9,
                                                           data=data,
                                                           code=200)

    @staticmethod
    def UpdateProjectTask200(data="None"):
        return ProjectTaskResponses.fill_success_responses(message_code=10,
                                                           data=data,
                                                           code=200)

    @staticmethod
    def UpdateProjectTask404(error="None"):
        return ProjectTaskResponses.fill_failed_responses(message_code=11,
                                                          error=error,
                                                          code=404)

    @staticmethod
    def UpdateProjectTask400(error="None"):
        return ProjectTaskResponses.fill_failed_responses(message_code=12,
                                                          error=error,
                                                          code=400)

    @staticmethod
    def DeleteProjectTask200(data="None"):
        return ProjectTaskResponses.fill_success_responses(message_code=13,
                                                           data=data,
                                                           code=200)

    @staticmethod
    def DeleteProjectTask404(error="None"):
        return ProjectTaskResponses.fill_failed_responses(message_code=14,
                                                          error=error,
                                                          code=404)
    @staticmethod
    def ProjectTasksAssignment200(data="None"):
        return ProjectTaskResponses.fill_success_responses(message_code=15,
                                                           data=data,
                                                           code=200)

    @staticmethod
    def ProjectTasksAssignment400(error="None"):
        return ProjectTaskResponses.fill_failed_responses(message_code=16,
                                                          error=error,
                                                          code=400)
