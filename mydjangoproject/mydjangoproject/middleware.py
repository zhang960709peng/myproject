from django.conf import settings
from django.http import HttpResponseForbidden,HttpResponse

class FilterIPMiddleware:
    def process_request(self,request):
        if request.META.get('HTTP_X_FORWARDED_FOR'):
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']

        print("ip=%s"%ip)

        if ip in settings.FORBIDDEN_IPS:
            return HttpResponseForbidden("你被禁止了")



class ExceptionMiddleware:
    def process_exception(self, request, exception):
        print(self)
        print(request)
        print(exception)

        return HttpResponse(exception)