# PROJECT TECHNOLOGIES
class ProjectTechnologyResponses:
    success_template: dict = {"response": {"message_code": "", "code": ""}, "data": ""}
    failed_template: dict = {"response": {"message_code": "", "code": ""}, "error": ""}

    @staticmethod
    def fill_failed_responses(message_code, error, code):
        response = ProjectTechnologyResponses.failed_template
        response["response"]["message_code"] = message_code
        response["response"]["code"] = code
        response["error"] = error
        return response

    @staticmethod
    def fill_success_responses(message_code, data, code):
        response = ProjectTechnologyResponses.success_template
        response["response"]["message_code"] = message_code
        response["response"]["code"] = code
        response["data"] = data
        return response

    @staticmethod
    def CreateProjectTechnology200(data="None"):
        return ProjectTechnologyResponses.fill_success_responses(message_code=1,  # "Project created successfully",
                                                          data=data,
                                                          code=200)

    @staticmethod
    def CreateProjectTechnology400(error="None"):
        return ProjectTechnologyResponses.fill_failed_responses(message_code=2,
                                                         # "Data sent is not valid to create a Project",
                                                         error=error,
                                                         code=400)
