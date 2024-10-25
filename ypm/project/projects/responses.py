# PROJECT
class ProjectResponses:
    success_template: dict = {"response": {"message_code": "", "code": ""}, "data": ""}
    failed_template: dict = {"response": {"message_code": "", "code": ""}, "error": ""}

    @staticmethod
    def fill_failed_responses(message_code, error, code):
        response = ProjectResponses.failed_template
        response["response"]["message_code"] = message_code
        response["response"]["code"] = code
        response["error"] = error
        return response

    @staticmethod
    def fill_success_responses(message_code, data, code):
        response = ProjectResponses.success_template
        response["response"]["message_code"] = message_code
        response["response"]["code"] = code
        response["data"] = data
        return response

    @staticmethod
    def CreateProject200(data="None"):
        return ProjectResponses.fill_success_responses(message_code=1,  # "Project created successfully",
                                                          data=data,
                                                          code=200)

    @staticmethod
    def CreateProject400(error="None"):
        return ProjectResponses.fill_failed_responses(message_code=2,
                                                         # "Data sent is not valid to create a Project",
                                                         error=error,
                                                         code=400)
    @staticmethod
    def DetailProject200(data="None"):
        return ProjectResponses.fill_success_responses(message_code=3,  # "Project created successfully",
                                                          data=data,
                                                          code=200)

    @staticmethod
    def DetailProject204(error="None"):
        return ProjectResponses.fill_failed_responses(message_code=4,
                                                         # "Data sent is not valid to create a Project",
                                                         error=error,
                                                         code=204)
    @staticmethod
    def ProjectTasks200(data="None"):
        return ProjectResponses.fill_success_responses(message_code=5,  # "Project created successfully",
                                                          data=data,
                                                          code=200)

    @staticmethod
    def ProjectTasks204(error="None"):
        return ProjectResponses.fill_failed_responses(message_code=6,
                                                         # "Data sent is not valid to create a Project",
                                                         error=error,
                                                         code=204)