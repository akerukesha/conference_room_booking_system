from django.http import HttpResponse
from functools import wraps

import codes, messages, string_utils
import json


def required_parameters(parameters_list):
    """
    Decorator to make a view only accept request with required parameters.
    :param parameters_list: list of required parameters.
    """
    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            if request.method == "POST":
                for parameter in parameters_list:
                    value = (
                        string_utils.empty_to_none(request.POST.get(parameter)
                            or request.FILES.get(parameter)))
                    if value is None:
                        return code_response(
                                codes.MISSING_REQUIRED_PARAMS,
                                message=messages.MISSING_REQUIRED_PARAMS.format(parameter))
            else:
                for parameter in parameters_list:
                    value = string_utils.empty_to_none(
                        request.GET.get(parameter))
                    if value is None:
                        return code_response(
                                codes.MISSING_REQUIRED_PARAMS,
                                message=messages.MISSING_REQUIRED_PARAMS.format(parameter))

            return func(request, *args, **kwargs)
        return inner
    return decorator


def http_response_with_json_body(body):
    return HttpResponse(body, content_type="application/json")


def http_response_with_json(json_object):
    return http_response_with_json_body(json.dumps(json_object))


def json_response():
    """
    Decorator that wraps response into json.
    """
    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            response = func(request, *args, **kwargs)
            if not ('code' in response):
                response['code'] = codes.OK
            response = http_response_with_json(response)
            return response
        return inner
    return decorator


def code_response(code, message=None, errors=None):
    result = {'code': code}
    if message:
        result['message'] = message
    if errors:
        result['errors'] = errors
    return result


def ok_response():
    return code_response(codes.OK)