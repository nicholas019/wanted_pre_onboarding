import jwt

from django.conf import settings
from django.http import JsonResponse

from users.models   import User
from company.models import Company


def user_login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get("Authorization", None)
            payload      = jwt.decode(access_token, settings.SECRET_KEY, algorithms = settings.ALGORITHM)
            user         = User.objects.get(id = payload["id"])
            request.user = user
        
        except jwt.exceptions.DecodeError:
            return JsonResponse({"message" : "INVALID TOKEN"}, status = 400)

        except User.DoesNotExist:
            return JsonResponse({"message" : "INVAILD_USER"}, status = 400)

        return func(self, request, *args, **kwargs)
    return wrapper

def company_login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get("Authorization", None)
            payload      = jwt.decode(access_token, settings.SECRET_KEY, algorithms = settings.ALGORITHM)
            user         = Company.objects.get(id = payload["id"])
            request.user = user
        
        except jwt.exceptions.DecodeError:
            return JsonResponse({"message" : "INVALID TOKEN"}, status = 400)

        except Company.DoesNotExist:
            return JsonResponse({"message" : "INVAILD_COMPANY"}, status = 400)

        return func(self, request, *args, **kwargs)
    return wrapper
