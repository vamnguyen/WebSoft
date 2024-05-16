from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from ..models import Token, Parameter

from ..messages.account import AccountMessage

class AuthorizationMiddleware(MiddlewareMixin):    
    def process_request(self, request):
        path = request.path
        
        if (path.split('/')[1] == 'admin'): return None
        if (path == '/account/log-in/'): return None
        
        token = request.META['HTTP_AUTHORIZATION']
        
        if token is None: 
            return JsonResponse(
                {
                    "success": False,
                    "message": AccountMessage.MSG1005,
                }, 
                status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,  
            )
            
        token = Token.objects.filter(Key=token).first()
        
        if token is None:
            return JsonResponse({
                "success": False,
                "message": AccountMessage.MSG1006,
            }, status=status.HTTP_401_UNAUTHORIZED, content_type='application/json')
            
        if (path == '/account/log-out/'): return None

        token_expire_time = Parameter.objects.filter(ParameterName='TokenExpireTime').first()
        if (token.Created + timedelta(hours=token_expire_time.Value)) < timezone.now():
            return JsonResponse({
                "success": False,
                "message": AccountMessage.MSG1007,
            }, status=status.HTTP_403_FORBIDDEN)
            
        return None           