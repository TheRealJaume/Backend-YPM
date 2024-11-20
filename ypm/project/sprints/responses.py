# PROJECT SPRINT
class ProjectSprintResponses:
    success_template: dict = {"response": {"message_code": "", "code": ""}, "data": ""}
    failed_template: dict = {"response": {"message_code": "", "code": ""}, "error": ""}

    @staticmethod
    def fill_failed_responses(message_code, error, code):
        response = ProjectSprintResponses.failed_template
        response["response"]["message_code"] = message_code
        response["response"]["code"] = code
        response["error"] = error
        return response

    @staticmethod
    def fill_success_responses(message_code, data, code):
        response = ProjectSprintResponses.success_template
        response["response"]["message_code"] = message_code
        response["response"]["code"] = code
        response["data"] = data
        return response

    @staticmethod
    def ProjectSprintOrganize200(data="None"):
        return ProjectSprintResponses.fill_success_responses(message_code=1,  # "ProjectSprint created successfully",
                                                             data=data,
                                                             code=200)

    @staticmethod
    def ProjectSprintOrganize400(error="None"):
        return ProjectSprintResponses.fill_failed_responses(message_code=2,
                                                            # "Data sent is not valid to create a ProjectSprint",
                                                            error=error,
                                                            code=400)

    @staticmethod
    def CheckStatusProjectSprint200(data="None"):
        return ProjectSprintResponses.fill_success_responses(message_code=3,  # "ProjectSprint created successfully",
                                                             data=data,
                                                             code=200)
    @staticmethod
    def ProjectSprintTasks200(data="None"):
        return ProjectSprintResponses.fill_success_responses(message_code=4,  # "ProjectSprint created successfully",
                                                             data=data,
                                                             code=200)
