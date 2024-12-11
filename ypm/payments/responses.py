class StripeResponses:
    success_template: dict = {"response": {"message_code": "", "code": ""}, "data": ""}
    failed_template: dict = {"response": {"message_code": "", "code": ""}, "error": ""}

    @staticmethod
    def fill_failed_responses(message_code, error, code):
        response = StripeResponses.failed_template
        response["response"]["message_code"] = message_code
        response["response"]["code"] = code
        response["error"] = error
        return response

    @staticmethod
    def fill_success_responses(message_code, data, code):
        response = StripeResponses.success_template
        response["response"]["message_code"] = message_code
        response["response"]["code"] = code
        response["data"] = data
        return response

    @staticmethod
    def CheckoutSession200(data="None"):
        return StripeResponses.fill_success_responses(message_code=1,
                                                      data=data,
                                                      code=200)

    @staticmethod
    def CheckoutSession400(error="None"):
        return StripeResponses.fill_failed_responses(message_code=2,
                                                     error=error,
                                                     code=400)

    @staticmethod
    def CheckoutSession500(error="None"):
        return StripeResponses.fill_failed_responses(message_code=3,
                                                     error=error,
                                                     code=500)


