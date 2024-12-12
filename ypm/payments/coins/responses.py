class UserCoinResponses:
    success_template: dict = {"response": {"message_code": "", "code": ""}, "data": ""}
    failed_template: dict = {"response": {"message_code": "", "code": ""}, "error": ""}

    @staticmethod
    def fill_failed_responses(message_code, error, code):
        response = UserCoinResponses.failed_template
        response["response"]["message_code"] = message_code
        response["response"]["code"] = code
        response["error"] = error
        return response

    @staticmethod
    def fill_success_responses(message_code, data, code):
        response = UserCoinResponses.success_template
        response["response"]["message_code"] = message_code
        response["response"]["code"] = code
        response["data"] = data
        return response

    @staticmethod
    def UpdateUserCoin200(data="None"):
        return UserCoinResponses.fill_success_responses(message_code=1,
                                                        data=data,
                                                        code=200)

    @staticmethod
    def UpdateUserCoin400(error="None"):
        return UserCoinResponses.fill_failed_responses(message_code=2,
                                                       error=error,
                                                       code=400)

    @staticmethod
    def UpdateUserCoin404(error="None"):
        return UserCoinResponses.fill_failed_responses(message_code=3,
                                                       error=error,
                                                       code=404)

    @staticmethod
    def RetrieveUserCoin200(data="None"):
        return UserCoinResponses.fill_success_responses(message_code=4,
                                                        data=data,
                                                        code=200)
    @staticmethod
    def RetrieveUserCoin404(error="None"):
        return UserCoinResponses.fill_failed_responses(message_code=5,
                                                       error=error,
                                                       code=404)
