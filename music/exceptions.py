from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler


class Conflict(APIException):
    status_code = 409
    default_code = "conflict"


def api_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        details = response.data
        if isinstance(details, dict) and "detail" in details:
            message = str(details["detail"])
            fields = {}
        else:
            message = "Перевірте правильність заповнення полів."
            fields = details
        response.data = {"error": {"message": message, "details": fields}}
    return response
