import jwt

from django.http  import JsonResponse
from django.conf  import settings

from users.models import User

def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):       
        if "Authorization" not in request.headers : 
            return JsonResponse ({"message" : "UNAUTHORIZED"}, status=401)

        access_token = request.headers["Authorization"]

        try:
            payload      = jwt.decode(access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            user         = User.objects.get(id = payload['user_id'])    
            request.user = user

        except jwt.exceptions.DecodeError:
            return JsonResponse({"massage" : "INVALID_TOKEN"}, status=401)

        except User.DoesNotExist:
            return JsonResponse({"message" : "INVALID_USER"}, status=401)

        return func(self, request, *args, **kwargs)

    return wrapper