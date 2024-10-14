class UserResponses:
    # Class methods for login viewset responses
    success_template: dict = {"response": {"message_code": "", "code": ""}, "data": ""}
    failed_template: dict = {"response": {"message_code": "", "code": ""}, "error": ""}

    @staticmethod
    def fill_failed_responses(message_code, error, code):
        response = UserResponses.failed_template
        response["response"]["message_code"] = message_code
        response["response"]["code"] = code
        response["error"] = error
        return response

    @staticmethod
    def fill_success_responses(message_code, data, code):
        response = UserResponses.success_template
        response["response"]["message_code"] = message_code
        response["response"]["code"] = code
        response["data"] = data
        return response

    @staticmethod
    def GetUserMe200(data="None"):
        return UserResponses.fill_success_responses(message_code=1,  # "Information sent is valid"
                                                    data=data,
                                                    code=200)

    @staticmethod
    def GetUserMe400(error="None"):
        return UserResponses.fill_failed_responses(message_code=2,  # "Introduced data is not valid",
                                                   error=error,
                                                   code=400)


class OnboardingResponses:
    # Class methods for login viewset responses
    success_template: dict = {"response": {"message_code": "", "code": ""}, "data": ""}
    failed_template: dict = {"response": {"message_code": "", "code": ""}, "error": ""}

    @staticmethod
    def fill_failed_responses(message_code, error, code):
        response = OnboardingResponses.failed_template
        response["response"]["message_code"] = message_code
        response["response"]["code"] = code
        response["error"] = error
        return response

    @staticmethod
    def fill_success_responses(message_code, data, code):
        response = OnboardingResponses.success_template
        response["response"]["message_code"] = message_code
        response["response"]["code"] = code
        response["data"] = data
        return response

    @staticmethod
    def UpdateOnboarding200(data="None"):
        return OnboardingResponses.fill_success_responses(message_code=1,
                                                          data=data,
                                                          code=200)
