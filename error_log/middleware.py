import traceback

from error_log.models import RequestError


class LogExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        RequestError.objects.create(
            exception_name=str(type(exception)),
            exception_value=str(exception),
            exception_tb='\n'.join(traceback.format_tb(exception.__traceback__)),  # noqa
            request_method=request.method,
            path=request.path,
            query=dict(request.GET),
            data=dict(request.POST)
        )
