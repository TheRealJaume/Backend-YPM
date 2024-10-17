class TechnologyResponses:
    success_template: dict = {"response": {"message_code": "", "code": ""}, "data": ""}
    failed_template: dict = {"response": {"message_code": "", "code": ""}, "error": ""}

    @staticmethod
    def fill_failed_responses(message_code, error, code):
        response = TechnologyResponses.failed_template
        response["response"]["message_code"] = message_code
        response["response"]["code"] = code
        response["error"] = error
        return response

    @staticmethod
    def fill_success_responses(message_code, data, code):
        response = TechnologyResponses.success_template
        response["response"]["message_code"] = message_code
        response["response"]["code"] = code
        response["data"] = data
        return response

    @staticmethod
    def CreateTechnology200(data="None"):
        return TechnologyResponses.fill_success_responses(message_code=1,  # "Technology created successfully",
                                                          data=data,
                                                          code=200)

    @staticmethod
    def CreateTechnology400(error="None"):
        return TechnologyResponses.fill_failed_responses(message_code=2,
                                                         # "Data sent is not valid to create a Technology",
                                                         error=error,
                                                         code=400)
