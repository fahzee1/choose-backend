import pdb
from models import Token
from django.http import JsonResponse



class TokenCheck(object):

    def process_request(middleware,request):
        token = request.META.get('HTTP_AUTHORIZATION',None)
        message = {'reason':'No User Token',
                   'success':False}
        if not token:
            response = JsonResponse(message)
            response.status_code = 403
            return response

        token = Token.objects.filter(key=token)
        if not token:
            response = JsonResponse(message)
            response.status_code=403
            return response
            

        return None



class CheckException(object):

    def process_exception(middleware,request,exception):
        print exception
        return None

