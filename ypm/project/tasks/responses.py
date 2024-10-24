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