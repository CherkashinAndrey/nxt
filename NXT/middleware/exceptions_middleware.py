from django.http import JsonResponse
from logging import getLogger
import json
from traceback import format_exc
from django.core.exceptions import ValidationError, PermissionDenied, FieldError


log = getLogger('ensomus')


class ConvertExceptionMiddleware(object):
    def process_view(self, request, view_func, view_args, view_kwargs):

        request.json_body = {}

        content_type = request.META.get('CONTENT_TYPE', 'text/html')

        if 'application/json' in content_type and hasattr(request, 'body') and request.body:
            try:
                request.json_body = json.loads(request.body)
            except Exception as e:
                log.error(u"Error in load json body: {}\n{}".format(e, request.body))
                return JsonResponse(data={"detail": str(e)}, status=400)

    def process_exception(self, request, exception):
        if 'application/json' in request.META.get('CONTENT_TYPE', 'text/html'):
            message = "Some error occurred."

            if isinstance(exception, ValidationError) or isinstance(exception, FieldError):
                code = 400
            elif isinstance(exception, PermissionDenied):
                code = 403
            else:
                code = 500

            if len(exception.args) == 1:
                message = exception.args
            elif len(exception.args) == 2:
                message, code = exception.args

            log.error("URL: {}. Request body:".format(request.path))
            log.error(getattr(request, 'json_body', getattr(request, 'body', 'Body is empty')))
            log.error(message)
            log.error(format_exc(exception))

            self._error_processed = True

            return JsonResponse({"detail": message}, status=code)

    def process_response(self, request, response):
        if getattr(response, 'status_code', 200) == 400 and not hasattr(self, '_error_processed'):
            log.error("URL: {}. Request body:".format(request.path))
            log.error(getattr(request, 'json_body', getattr(request, 'body', 'Body is empty')))
            log.error(response.content)

        return response