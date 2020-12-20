import time,json
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse
from meterApi.des_verify import des_descrypt

from apps.models import Params

class chkToken(MiddlewareMixin):

    def process_request(self,request):
        json_data={'code':'1','msg':'ok'}
        token_get=request.META.get("HTTP_TOKEN")
        token_get=des_descrypt(token_get)
        timespan_token=token_get.split('_'.encode(encoding="utf-8"), 1)[1]
        timespan_token_=int(timespan_token)
        timespan_get=request.META.get("HTTP_TIMESPAN")
        if(int(timespan_get)!=timespan_token_):
            #print("Error",timespan_get,timespan_token)
            json_data={'code':'-1','msg':'myMiddleware.py:Timespan is wrong'}
            return HttpResponse(json.dumps(json_data))
        if(int(time.time())-timespan_token_>600):
            #print("Error",timespan_get,timespan_token)
            json_data={'code':'-2','msg':'myMiddleware.py:Timespan is too long'}
            return HttpResponse(json.dumps(json_data))
        #return HttpResponse(json.dumps(json_data))
 
    def process_response(self,request,response):
        return response
