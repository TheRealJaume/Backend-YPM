class CompanyDepartmentResponses:
    success_template: dict = {"response": {"message_code": "", "code": ""}, "data": ""}
    failed_template: dict = {"response": {"message_code": "", "code": ""}, "error": ""}

    @staticmethod
    def fill_failed_responses(message_code, error, code):
        response = CompanyDepartmentResponses.failed_template
        response["response"]["message_code"] = message_code
        response["response"]["code"] = code
        response["error"] = error
        return response

    @staticmethod
    def fill_success_responses(message_code, data, code):
        response = CompanyDepartmentResponses.success_template
        response["response"]["message_code"] = message_code
        response["response"]["code"] = code
        response["data"] = data
        return response

    @staticmethod
    def CreateCompanyDepartment200(data="None"):
        return CompanyDepartmentResponses.fill_success_responses(message_code=1,  # "Department created successfully",
                                                                 data=data,
                                                                 code=200)

    @staticmethod
    def CreateCompanyDepartment400(error="None"):
        return CompanyDepartmentResponses.fill_failed_responses(message_code=2, # "Data sent is not valid to create a Department",
                                                                error=error,
                                                                code=400)
