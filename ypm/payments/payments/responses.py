class UserPaymentsResponses:
    success_template: dict = {"response": {"message_code": "", "code": ""}, "data": ""}
    failed_template: dict = {"response": {"message_code": "", "code": ""}, "error": ""}

    @staticmethod
    def fill_failed_responses(message_code, error, code):
        response = UserPaymentsResponses.failed_template
        response["response"]["message_code"] = message_code
        response["response"]["code"] = code
        response["error"] = error
        return response

    @staticmethod
    def fill_success_responses(message_code, data, code):
        response = UserPaymentsResponses.success_template
        response["response"]["message_code"] = message_code
        response["response"]["code"] = code
        response["data"] = data
        return response

    @staticmethod
    def RetrieveUserPayments200(data="None"):
        return UserPaymentsResponses.fill_success_responses(message_code=1,
                                                            data=data,
                                                            code=200)

    @staticmethod
    def RetrieveUserPayments404(error="None"):
        return UserPaymentsResponses.fill_failed_responses(message_code=2,
                                                           error=error,
                                                           code=404)

    @staticmethod
    def UpdateUserPayments200(data="None"):
        return UserPaymentsResponses.fill_success_responses(message_code=3,
                                                            data=data,
                                                            code=200)

    @staticmethod
    def UpdateUserPayments404(error="None"):
        return UserPaymentsResponses.fill_failed_responses(message_code=4,
                                                           error=error,
                                                           code=404)

    @staticmethod
    def UpdateUserPayments400(error="None"):
        return UserPaymentsResponses.fill_failed_responses(message_code=5,
                                                           error=error,
                                                           code=400)
    @staticmethod
    def UpdateUserPayments500(error="None"):
        return UserPaymentsResponses.fill_failed_responses(message_code=6,
                                                           error=error,
                                                           code=500)

    @staticmethod
    def ListUserPayments200(data="None"):
        return UserPaymentsResponses.fill_success_responses(message_code=7,
                                                            data=data,
                                                            code=200)

    @staticmethod
    def ListUserPayments204(error="None"):
        return UserPaymentsResponses.fill_failed_responses(message_code=8,
                                                           error=error,
                                                           code=204)