from django.core.exceptions import PermissionDenied
from django.http import Http404, JsonResponse
from rest_framework.exceptions import NotFound, PermissionDenied as PD, NotAuthenticated, MethodNotAllowed
from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework.views import exception_handler


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
    print('exception in view:', context['view'])
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    print('exception:', exc)
    if isinstance(exc, PD):
        return error_response(code=1003, msg='Permission not allowed.')

    if isinstance(exc, MethodNotAllowed):
        return error_response(code=1005, msg='Method not allowed.')

    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    return response
