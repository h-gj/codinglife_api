from django.core.exceptions import PermissionDenied
from django.http import Http404, JsonResponse, HttpResponseServerError
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied as PD, NotAuthenticated, MethodNotAllowed
from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework.views import exception_handler


class DDAPIException(Exception):
    """业务异常类"""

    code = status.HTTP_500_INTERNAL_SERVER_ERROR
    message = ''

    def __init__(self, code=None, message=None):
        super().__init__()
        if code is not None:
            self.code = code
        if message is not None:
            self.message = message


def error_response(code=1001, data=None, msg=''):
    wrapper_data = {
        'code': code,
        'status': 'error',
        'data': data,
        'msg': msg
    }
    return JsonResponse(wrapper_data)


from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    print('Exception ===>', exc)
    print('Type of exception ===>:', type(exc))

    if isinstance(exc, PD):
        return error_response(code=1003, msg='Permission not allowed.')

    if isinstance(exc, MethodNotAllowed):
        return error_response(code=1005, msg='Method not allowed.')

    if isinstance(exc, NotAuthenticated):
        return error_response(code=1003, msg='Authentication credentials not provided.')

    if isinstance(exc, DDAPIException):
        return error_response(code=exc.code, msg=exc.message)

    if isinstance(exc, AttributeError):
        return error_response(code=1005, msg='Internal server error.')

    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    return response
