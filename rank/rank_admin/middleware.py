from django.utils.deprecation import MiddlewareMixin
from django.http import Http404


class StaffUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if 'r-admin' in request.path:
            if request.user.is_staff is False:
                raise Http404
