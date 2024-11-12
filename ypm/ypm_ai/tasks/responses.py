# TASK
class TaskResponses:
    success_template: dict = {"response": {"message_code": "", "code": ""}, "data": ""}
    failed_template: dict = {"response": {"message_code": "", "code": ""}, "error": ""}

    @staticmethod
    def fill_failed_responses(message_code, error, code):
        response = TaskResponses.failed_template
        response["response"]["message_code"] = message_code
        response["response"]["code"] = code
        response["error"] = error
        return response

    @staticmethod
    def fill_success_responses(message_code, data, code):
        response = TaskResponses.success_template
        response["response"]["message_code"] = message_code
        response["response"]["code"] = code
        response["data"] = data
        return response

    @staticmethod
    def CreateTask200(data="None"):
        return TaskResponses.fill_success_responses(message_code=1,  # "Task created successfully",
                                                          data=data,
                                                          code=200)

    @staticmethod
    def CreateTask400(error="None"):
        return TaskResponses.fill_failed_responses(message_code=2,
                                                         # "Data sent is not valid to create a Task",
                                                         error=error,
                                                         code=400)
    @staticmethod
    def DetailTask200(data="None"):
        return TaskResponses.fill_success_responses(message_code=3,  # "Task created successfully",
                                                          data=data,
                                                          code=200)

    @staticmethod
    def DetailTask204(error="None"):
        return TaskResponses.fill_failed_responses(message_code=4,
                                                         # "Data sent is not valid to create a Task",
                                                         error=error,
                                                         code=400)