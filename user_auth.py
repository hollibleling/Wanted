import jwt, json

from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from my_settings import SECRET_KEY
from user.models import User

def authentication(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authorization', None)
            if not access_token:
                return JsonResponse({ 'MESSAGE' : 'NO TOKEN' }, status = 403)

            payload = jwt.decode(access_token, SECRET_KEY, 'HS256')
            user_id = payload['id']

            user = User.objects.get(id = user_id)
            request.user = user.id

        except jwt.exceptions.DecodeError:
            return JsonResponse({ 'MESSAGE' : 'INVALID TOKEN' }, status = 403)

        except User.DoesNotExist:
            return JsonResponse({ 'MESSAGE' : 'INVALID USER' }, status = 403)

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status = 400)

        return func(self, request, *args, **kwargs)

    return wrapper

