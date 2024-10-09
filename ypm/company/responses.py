class CompanyResponses:
    success_template: dict = {"response": {"message_code": "", "code": ""}, "data": ""}
    failed_template: dict = {"response": {"message_code": "", "code": ""}, "error": ""}

    @staticmethod
    def fill_failed_responses(message_code, error, code):
        response = CompanyResponses.failed_template
        response["response"]["message_code"] = message_code
        response["response"]["code"] = code
        response["error"] = error
        return response

    @staticmethod
    def fill_success_responses(message_code, data, code):
        response = CompanyResponses.success_template
        response["response"]["message_code"] = message_code
        response["response"]["code"] = code
        response["data"] = data
        return response

    @staticmethod
    def CreateCompany200(data="None"):
        return CompanyResponses.fill_success_responses(message_code=1, #"Company created successfully",
                                                       data=data,
                                                       code=200)

    @staticmethod
    def CreateCompany400(error="None"):
        return CompanyResponses.fill_failed_responses(message_code=2, #"Data sent is not valid to create a company",
                                                      error=error,
                                                      code=400)
