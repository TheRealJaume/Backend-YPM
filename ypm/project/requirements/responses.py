# PROJECT REQUIREMENT
class ProjectRequirementResponses:
    success_template: dict = {"response": {"message_code": "", "code": ""}, "data": ""}
    failed_template: dict = {"response": {"message_code": "", "code": ""}, "error": ""}

    @staticmethod
    def fill_failed_responses(message_code, error, code):
        response = ProjectRequirementResponses.failed_template
        response["response"]["message_code"] = message_code
        response["response"]["code"] = code
        response["error"] = error
        return response

    @staticmethod
    def fill_success_responses(message_code, data, code):
        response = ProjectRequirementResponses.success_template
        response["response"]["message_code"] = message_code
        response["response"]["code"] = code
        response["data"] = data
        return response

    @staticmethod
    def CreateProjectRequirements200(data="None"):
        return ProjectRequirementResponses.fill_success_responses(message_code=1,  # "Project created successfully",
                                                                  data=data,
                                                                  code=200)

    @staticmethod
    def CreateProjectRequirements400(error="None"):
        return ProjectRequirementResponses.fill_failed_responses(message_code=2,
                                                                 # "Data sent is not valid to create a Project",
                                                                 error=error,
                                                                 code=400)

    @staticmethod
    def TranscriptProjectRequirements200(data=None):
        return ProjectRequirementResponses.fill_success_responses(message_code=4,  # "Project created successfully",
                                                                  data=data,
                                                                  code=200)

    @staticmethod
    def CheckStatusTranscription200(data=None):
        return ProjectRequirementResponses.fill_success_responses(message_code=5,  # "Project created successfully",
                                                                  data=data,
                                                                  code=200)

    @staticmethod
    def CheckStatusTranscription400(error="None"):
        return ProjectRequirementResponses.fill_failed_responses(message_code=6,  # "Project created successfully",
                                                                 error=error,
                                                                 code=400)

    @staticmethod
    def TranscriptProjectRequirements400(error="None"):
        return ProjectRequirementResponses.fill_failed_responses(message_code=7,
                                                                 # "Data sent is not valid to create a Project",
                                                                 error=error,
                                                                 code=400)

    @staticmethod
    def UpdateProjectRequirement200(data="None"):
        return ProjectRequirementResponses.fill_success_responses(message_code=8,
                                                                  data=data,
                                                                  code=200)

    @staticmethod
    def UpdateProjectRequirement404(error="None"):
        return ProjectRequirementResponses.fill_failed_responses(message_code=9,
                                                                 error=error,
                                                                 code=404)

    @staticmethod
    def UpdateProjectRequirement400(error="None"):
        return ProjectRequirementResponses.fill_failed_responses(message_code=10,
                                                                 error=error,
                                                                 code=400)

    @staticmethod
    def DeleteProjectRequirement200(data="None"):
        return ProjectRequirementResponses.fill_success_responses(message_code=11,
                                                                  data=data,
                                                                  code=200)

    @staticmethod
    def DeleteProjectRequirement404(error="None"):
        return ProjectRequirementResponses.fill_failed_responses(message_code=12,
                                                                 error=error,
                                                                 code=404)
